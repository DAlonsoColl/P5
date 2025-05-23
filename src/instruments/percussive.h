#ifndef INSTRUMENT_PERCUSSIVE
#define INSTRUMENT_PERCUSSIVE

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc
{
    class PercussiveInstrument : public Instrument
    {
        EnvelopeADSR adsr;
        unsigned int index;
        float A;
        std::vector<float> tbl;
        float f0, increment, phas;

    public:
        PercussiveInstrument(const std::string &param = "");
        void command(long cmd, long note, long velocity = 10);
        const std::vector<float> &synthesize();
        bool is_active() const { return bActive; }

    private:
        float getInterpolatedValue(const float phas);
    };
}

#endif
