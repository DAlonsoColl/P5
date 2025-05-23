#include <iostream>
#include <math.h>
#include <string.h>
#include "SenoFMSimple.h"
#include "keyvalue.h"
#include "wavfile_mono.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

// Constructor initializes the ADSR envelope and sets default parameters.
SenoFMSimple::SenoFMSimple(const std::string &param)
    : adsr(SamplingRate, param)
{
    bActive = false;
    x.resize(BSIZE);

    /*
      Use KeyValue class to parse 'param' and configure instrument parameters.
      Refer to keyvalue.h for details.
    */
    KeyValue kv(param);

    // Default value if 'N' is not specified in 'param'.
    if (!kv.to_int("N", N))
        N = 40;

    // Modulation index
    if (!kv.to_float("I", I))
        I = 1;

    // Default values for N1 and N2.
    if (!kv.to_float("N1", N1))
        N1 = 1;

    if (!kv.to_float("N2", N2))
        N2 = 1;

    // initialize default source & modulated table values
    tbl_signal.resize(N);
    tbl_modulation.resize(N);
    float phase = 0, step = 2 * M_PI / (float)N;
    for (int i = 0; i < N; ++i)
    {
        tbl_signal[i] = sin(phase);
        tbl_modulation[i] = sin(phase);
        phase += step;
    }

    // initialize table indexes to 0
    modulation_table_index = 0;
    signal_table_index = 0;
}

// Process commands to start, sustain, or release a note.
void SenoFMSimple::command(long cmd, long note, long vel)
{
    if (cmd == 9)
    { //'Key' pressed: trigger attack phase
        bActive = true;
        adsr.start();

        // computation of signal table index increments
        float fc = pow(2, ((float)note - 69) / 12) * 440; // Convert note to frequency (Hz)
        increment_signal_table = ((fc / SamplingRate) * tbl_signal.size());

        // computation of modulation table index increments

        // we know that fc = fm * (N1/N2) so fm = fc * (N2/N1)
        float fm = fc * (N2 / N1);
        increment_modulation_table = ((fm / SamplingRate) * tbl_signal.size());

        if (vel > 127)
            vel = 127;

        A = vel / 127.;
    }
    else if (cmd == 8)
    { //'Key' released: trigger release phase
        adsr.stop();
    }
    else if (cmd == 0)
    {
        adsr.end();
    }
}

// Synthesize the waveform using FM synthesis
const vector<float> &SenoFMSimple::synthesize()
{
    if (not adsr.active())
    {
        x.assign(x.size(), 0);
        bActive = false;
        return x;
    }
    else if (not bActive)
        return x;

    // create intermediate float array with modulated signal values (interpolated)
    std::vector<float> modulated_values; // create array and resize
    modulated_values.resize(x.size());

    // assign values
    for (int i = 0; i < x.size(); i++)
    {
        bool condition = (modulation_table_index == int(modulation_table_index));
        modulated_values[i] = condition ? tbl_modulation[modulation_table_index] : I * getInterpolatedValue(modulation_table_index, string("modulation_table"));
        modulation_table_index += increment_modulation_table;
        // control index bounds
        if (modulation_table_index >= (float)tbl_modulation.size())
        {
            modulation_table_index -= (float)tbl_modulation.size();
        }
    }

    // populate x array with signal values: x[i]= A * sin(index_signal_table + I * sin(index_modulation_table))
    for (int i = 0; i < x.size(); i++)
    {
        float general_index;
        // check wether signal_table_index is + or -
        if (signal_table_index < 0)
        {
            general_index = signal_table_index + tbl_signal.size();
        }
        else
        {
            general_index = signal_table_index;
        }
        bool condition = (general_index == int(general_index));
        x[i] = condition ? tbl_signal[general_index] : getInterpolatedValue(general_index, string("signal_table"));
        signal_table_index += increment_signal_table + modulated_values[i];

        // control index bounds
        if (signal_table_index >= (float)tbl_signal.size())
        {
            signal_table_index -= (float)tbl_signal.size();
        }
    }
    return x;
}

float SenoFMSimple::getInterpolatedValue(const float phas, string table)
{
    int tbl_size;
    std::vector<float> *tbl;
    if (table == "signal_table")
    {
        tbl_size = tbl_signal.size();
        tbl = &tbl_signal;
    }
    else
    {
        tbl_size = tbl_modulation.size();
        tbl = &tbl_modulation;
    }

    size_t lowerIndex = static_cast<size_t>(std::floor(phas));
    size_t upperIndex = static_cast<size_t>(std::ceil(phas));

    // Boundary conditions for lowerIndex and upperIndex
    if (lowerIndex >= tbl_size || upperIndex >= tbl_size)
    {
        lowerIndex = tbl_size - 1;
        upperIndex = 0;
    }

    // Interpolate between tbl[lowerIndex] and tbl[upperIndex]
    float lowerValue = (*tbl)[lowerIndex];
    float upperValue = (*tbl)[upperIndex];

    // compute interpolation weights
    float interval_length = upperIndex - lowerIndex;
    float lower_index_weight = (upperIndex - phas) / interval_length;
    float upper_index_weight = (phas - lowerIndex) / interval_length;

    // computation of interpolated value
    float interpolated_value = lower_index_weight * lowerValue + upper_index_weight * upperValue;

    return interpolated_value;
}
