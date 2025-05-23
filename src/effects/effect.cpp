#include <iostream>
#include "effect.h"
#include "tremolo.h"
#include "vibrato.h"
#include "fuzz.h"

/*
  For each new effect:
  - Add the header in this file
  - Add the call to the constructor in get_effect() (also in this file)
  - Add the source file to src/meson.build
*/

using namespace std;

#include <iostream>
#include "effect.h"
#include "tremolo.h"
#include "vibrato.h"
#include "fuzz.h"  // Incluir el header del efecto Fuzz

using namespace std;

namespace upc {
  Effect *get_effect(const string &name, const string &parameters) {
    Effect *pEffect = nullptr; // Usar nullptr en lugar de 0 para punteros

    if (name == "Tremolo") {
      pEffect = static_cast<Effect *>(new Tremolo(parameters));
    }
    else if (name == "Vibrato") {
      pEffect = static_cast<Effect *>(new Vibrato(parameters));
    }
    else if (name == "Fuzz") {
      pEffect = static_cast<Effect *>(new Fuzz(parameters));
    }

    return pEffect;
  }
}

