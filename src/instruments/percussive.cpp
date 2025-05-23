#include <iostream>
#include <math.h>
#include "percussive.h"
#include "keyvalue.h"
#include <stdlib.h>

using namespace upc;
using namespace std;

PercussiveInstrument::PercussiveInstrument(const std::string &param)
    : adsr(SamplingRate, param)
{
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(param);
  int N;
  if (!kv.to_int("N", N))
    N = 40; // default value

  int interpolation;
  if (!kv.to_int("I", interpolation))
    interpolation = 0; // default value

  tbl.resize(N);
  float phase = 0, step = 2 * M_PI / (float)N;
  index = 0;
  for (int i = 0; i < N; ++i)
  {
    tbl[i] = sin(phase);
    phase += step;
  }
}

void PercussiveInstrument::command(long cmd, long note, long vel)
{
  f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f); // convertion of NOTE to FREQ

  if (cmd == 9)
  { //'Key' pressed: attack begins
    bActive = true;
    adsr.start();
    index = 0;
    phas = 0.0f;
    increment = ((f0 / SamplingRate) * tbl.size());
    A = vel / 127.0f;
  }
  else if (cmd == 8)
  { //'Key' released: sustain ends, release begins
    adsr.stop();
  }
  else if (cmd == 0)
  { // Sound extinguished without waiting for release to end
    adsr.end();
  }
}

const vector<float> &PercussiveInstrument::synthesize()
{
  if (not adsr.active())
  {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i)
  {
    phas += increment;
    if (std::floor(phas) == phas)
    {
      x[i] = A * tbl[round(phas)];
    }
    else
    {
      x[i] = A * getInterpolatedValue(phas);
    }
    while (phas >= tbl.size())
      phas = phas - tbl.size();
  }
  adsr(x);

  return x;
}

float PercussiveInstrument::getInterpolatedValue(const float phas)
{
  int tbl_size = tbl.size();
  size_t lowerIndex = static_cast<size_t>(std::floor(phas));
  size_t upperIndex = static_cast<size_t>(std::ceil(phas));

  if (lowerIndex >= tbl_size || upperIndex >= tbl_size)
  {
    lowerIndex = tbl_size - 1;
    upperIndex = 0;
  }

  float lowerValue = tbl[lowerIndex];
  float upperValue = tbl[upperIndex];

  return (lowerValue + upperValue) / 2;
}
