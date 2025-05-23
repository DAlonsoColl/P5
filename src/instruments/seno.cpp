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

  /*
    You can use the class keyvalue to parse "param" and configure your instrument.
    Take a Look at keyvalue.h
  */
  KeyValue kv(param);
  int N;
  if (!kv.to_int("N", N))
    N = 40; // default value

  /*additionally, we can add another parameter that dictates the mode of tbl values extractions where:

    - 0 == no interpolation
    - 1 == interpolation (first_value + second_value)/2
  */

  if (kv("I") != "false")
    Interpolation = false; // default value
  else
  {
    Interpolation = true;
  }

  /*we can also implemented seno instrument to be percussive (with exponential final decay)*/
  if (kv("percussive") == "true")
    percussive = true; // default value
  else
  {
    percussive = false;
  }

  // Create a tbl with one period of a sinusoidal wave
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
  f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f); // convertion of NOTE to FREQ

  if (cmd == 9)
  { //'Key' pressed: attack begins
    bActive = true;
    adsr.start();
    index = 0;
    phas = 0.0f;
    increment = ((f0 / SamplingRate) * tbl.size());
    A = vel / 127.;
    // A = std::clamp(static_cast<float>(vel) / 127.0f, 0.0f, 1.0f);
  }
  else if (cmd == 8)
  { //'Key' released: sustain ends, release begins
    adsr.stop();
    end_hit = true;
  }
  else if (cmd == 0)
  { // Sound extinguished without waiting for release to end
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

  /*En general, al recorrer la tabla con los saltos adecuados para producir una cierta
  frecuencia fundamental, será necesario acceder a índices no enteros de la tabla. Es
  decir, el valor deseado no se corresponde con ninguno de los que están almacenados
  en ella, sino a uno intermedio entre dos que sí lo están (que pueden ser el último y el
  primero...).

  ◦ En primera aproximación, puede redondear el índice requerido a entero y usar
  para la muestra uno de los valores almacenados en la tabla. <-- LO QUE ESTAMOS USANDO AHORA

  ⋄ Pero esta solución introduce una distorsión que es claramente audible.

  ◦ Como trabajo de ampliación, se propone calcular el valor de la muestra como
  interpolación lineal entre los valores inmediatamente anterior y posterior al índice
  deseado (pero recuerde que el siguiente del último es el primero...)*/
  for (unsigned int i = 0; i < x.size(); ++i)
  {
    phas += increment;
    /*if percussive == true and note end has been hit*/
    if (percussive && end_hit)
    {
      if (std::floor(phas) == phas || !Interpolation)
      {
        x[i] = A * tbl[round(phas)] * pow(0.99935, (int)interrupted_index);
        interrupted_index++;
      }
      else // phas is a non intger, we must interpolate
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
      else // phas is a non intger, we must interpolate
      {
        x[i] = A * getInterpolatedValue(phas);
      }
    }
    while (phas >= tbl.size())
      phas = phas - tbl.size();
  }
  adsr(x); // apply envelope to x and update internal status of ADSR

  return x;
}

/*en caso de quer realizar la ampliación como dice arriba, podemos realizar la interpolación
   de la siguiente manera:*/

float InstrumentSeno::getInterpolatedValue(const float phas)
{

  int tbl_size = tbl.size();
  size_t lowerIndex = static_cast<size_t>(std::floor(phas));
  size_t upperIndex = static_cast<size_t>(std::ceil(phas));

  // Boundary conditions for lowerIndex and upperIndex
  if (lowerIndex >= tbl_size || upperIndex >= tbl_size)
  {
    lowerIndex = tbl_size - 1;
    upperIndex = 0;
  }

  // Interpolate between tbl[lowerIndex] and tbl[upperIndex]
  float lowerValue = tbl[lowerIndex];
  float upperValue = tbl[upperIndex];

  return (lowerValue + upperValue) / 2;
}
