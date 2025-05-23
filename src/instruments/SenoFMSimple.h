#ifndef INSTRUMENT_SENO_FM_SIMPLE
#define INSTRUMENT_SENO_FM_SIMPLE

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc
{
    class SenoFMSimple : public Instrument
    {
        EnvelopeADSR adsr; // ADSR envelope generator
        float A, increment_modulation_table,
            increment_signal_table, modulation_table_index, signal_table_index, N1, N2, I;         // Parameters for frequency modulation
        int N;                                         // Various counters and settings
        std::vector<float> tbl_signal, tbl_modulation; // Tables for waveform and temporary storage

    public:
        // Constructor that initializes parameters based on optional input 'param'.
        SenoFMSimple(const std::string &param = "");

        // Process commands to start, sustain, or release a note.
        void command(long cmd, long note, long velocity = 1);

        // Synthesize and return a vector of float samples.
        const std::vector<float> &synthesize();

        // Check if the instrument is currently active.
        bool is_active() const { return bActive; }

    private:
        // internal class function for interpolation between tbl[] values
        float getInterpolatedValue(const float index, std::string string);
    };
}

#endif
