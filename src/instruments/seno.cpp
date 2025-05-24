#include <iostream>
#include <math.h>
#include "seno.h"
#include "keyvalue.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

InstrumentSeno::InstrumentSeno(const std::string &param)
    : adsr(SamplingRate, param)
{
  bActive = false;
  x.resize(BSIZE);

  
  KeyValue kv(param);
  int N;
  if (!kv.to_int("N", N))
    N = 40; 

  if (kv("I") != "false")
    Interpolation = false; // default value
  else
  {
    Interpolation = true;
  }

  
  if (kv("percussive") == "true")
    percussive = true; // default value
  else
  {
    percussive = false;
  }

  tbl.resize(N);
  float phase = 0, step = 2 * M_PI / (float)N;
  index = 0;
  for (int i = 0; i < N; ++i)
  {
    tbl[i] = sin(phase);
    phase += step;
  }
}

void InstrumentSeno::command(long cmd, long note, long vel)
{
  f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f); 

  if (cmd == 9)
  { 
    bActive = true;
    adsr.start();
    index = 0;
    phas = 0.0f;
    increment = ((f0 / SamplingRate) * tbl.size());
    A = vel / 127.;
    // A = std::clamp(static_cast<float>(vel) / 127.0f, 0.0f, 1.0f);
  }
  else if (cmd == 8)
  { 
    adsr.stop();
    end_hit = true;
  }
  else if (cmd == 0)
  { 
    adsr.end();
  }
}

const vector<float> &InstrumentSeno::synthesize()
{
  if (not adsr.active())
  {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  /* Como trabajo de ampliación,calculamos el valor de la muestra como
  interpolación lineal entre los valores inmediatamente anterior y posterior al índice
  deseado */

  for (unsigned int i = 0; i < x.size(); ++i)
  {
    phas += increment;
    if (percussive && end_hit)
    {
      if (std::floor(phas) == phas || !Interpolation)
      {
        x[i] = A * tbl[round(phas)] * pow(0.99935, (int)interrupted_index);
        interrupted_index++;
      }
      else 
      {
        x[i] = A * getInterpolatedValue(phas) * pow(0.99935, (int)interrupted_index);
        interrupted_index++;
      }
    }
    else
    {
      if (std::floor(phas) == phas || !Interpolation)
      {
        x[i] = A * tbl[round(phas)];
      }
      else 
      {
        x[i] = A * getInterpolatedValue(phas);
      }
    }
    while (phas >= tbl.size())
      phas = phas - tbl.size();
  }
  adsr(x); 
  return x;
}

float InstrumentSeno::getInterpolatedValue(const float phas)
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
