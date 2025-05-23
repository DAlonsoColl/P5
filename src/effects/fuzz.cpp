#include <iostream>
#include <math.h>
#include "fuzz.h"
#include "keyvalue.h"

static float SamplingRate = 44100;

using namespace upc;
using namespace std;

Fuzz::Fuzz(const std::string &param) {
  KeyValue kv(param);

  if (!kv.to_float("gain", gain))
    gain = 1.0; // default gain

  if (!kv.to_float("threshold", threshold))
    threshold = 0.5; // default threshold

  if (!kv.to_float("knee_width", knee_width))
    knee_width = 0.1; // default knee width

  if (!kv.to_float("mix", mix))
    mix = 1.0; // default mix

  if (!kv.to_float("hf_damp", hf_damp))
    hf_damp = 0.5; // default high-frequency damping

  if (!kv.to_float("oversampling", oversampling))
    oversampling = 4; // default oversampling factor

  inc_fase = 2 * M_PI * 100 / SamplingRate;

  s1 = 0.0;
  x1 = 0.0;
  s2 = 0.0;
  x2 = 0.0;
}

void Fuzz::command(unsigned int comm) {
  if (comm == 1) fase = 0;
}

void Fuzz::operator()(std::vector<float> &x){
  for (unsigned int i = 0; i < x.size(); i++) {
    float s0 = s1;

    s1 = 2.0f * gain * x[i] - x1 - s2 - x2;

    x1 = s0;
    x2 = s1;

    // Aplicar una curva de transferencia para generar el efecto de distorsión
    float fuzz = tanh(s1 * 0.5f * hf_damp);

    // Mezclar la señal distorsionada con la señal original
    x[i] = (1 - mix) * x[i] + mix * fuzz;
  }
}