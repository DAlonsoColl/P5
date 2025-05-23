#include <iostream>
#include "instrument_dumb.h"
#include "seno.h"
#include "percussive.h"
#include "senoFM.h"
#include "SenoFMSimple.h"

/*
  For each new instrument:
  - Add the header in this file
  - Add the call to the constructor in get_instrument() (also in this file)
  - Add the source file to src/meson.build
*/

using namespace std;

namespace upc {
  Instrument * get_instrument(const string &name,
			      const string &parameters) {
    Instrument * pInst = 0;
    //    cout << name << ": " << parameters << endl;
    if (name == "InstrumentDumb") {
      pInst = (Instrument *) new InstrumentDumb(parameters);
    }
    if (name == "InstrumentSeno") {
      pInst = (Instrument *) new InstrumentSeno(parameters);
    }
    if (name == "PercussiveInstrument") {
      pInst = (Instrument *) new PercussiveInstrument(parameters);
    }
    if (name == "SenoFM") {
      pInst = (Instrument *) new SenoFM(parameters);
    }
    if (name == "SenoFMSimple") {
      pInst = (Instrument *) new SenoFMSimple(parameters);
    }
    return pInst;
  }
}
