#include <iostream>
#include <math.h>
#include "senoFM.h"
#include "keyvalue.h"
#include "wavfile_mono.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

// Constructor initializes the ADSR envelope and sets default parameters.
SenoFM::SenoFM(const std::string &param)
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

    // Attack, Decay, Sustain, Release parameters for ADSR envelope.
    if (!kv.to_float("ADSR_A", adsr_a))
        adsr_a = 0.1;

    if (!kv.to_float("ADSR_D", adsr_d))
        adsr_d = 0.05;

    if (!kv.to_float("ADSR_S", adsr_s))
        adsr_s = 0.5;

    if (!kv.to_float("ADSR_R", adsr_r))
        adsr_r = 0.1;

    // Modulation index 1.
    if (!kv.to_float("I1", I1))
        I1 = 1;

    // Default values for N1 and N2.
    if (!kv.to_float("N1", N1))
        N1 = 1;

    if (!kv.to_float("N2", N2))
        N2 = 1;

    // Default envelope for additional parameters.
    if (!kv.to_float("envelope", envelope))
        envelope = 0;

    // Configure ADSR envelope based on 'envelope'.
    if (envelope == -1)
    {
        adsr.set(adsr_a, 0, adsr_s, adsr_r, 1.5F);
    }

    modulation_phase = 0;
    index_sensitivity = 0;

    std::string file_name;
    static string kv_null;
    waveform_table.resize(N);
    float phase = 0, step = 2 * M_PI / (float)N;
    index = 0;
    for (int i = 0; i < N; ++i)
    {
        waveform_table[i] = sin(phase);
        phase += step;
    }
}

// Process commands to start, sustain, or release a note.
void SenoFM::command(long cmd, long note, long vel)
{
    if (cmd == 9)
    { //'Key' pressed: trigger attack phase
        bActive = true;
        adsr.start();
        float f0note = pow(2, ((float)note - 69) / 12) * 440; // Convert note to frequency (Hz)
        N_notes = 1 / f0note * SamplingRate;                    // Note period in samples
        index_step = (float)N / N_notes;                        // Table step per note period

        // Reset counters/phases
        index = 0;
        index_sensitivity = 0;
        modulation_phase = 0;
        decay_count = 0;
        decay_count_I = 0;

        fm_modulation = f0note * N2 / N1;                         // Modulating frequency
        phase_step_size = 2 * M_PI * fm_modulation / SamplingRate; // Step of the modulating sine wave

        note_int = round(N_notes);
        temp.resize(note_int);

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
        // Faster release, ensuring smooth transition
        adsr.set(adsr_s, adsr_a, adsr_d, adsr_r / 4, 1.5F);
        adsr.stop();
    }
}

// Synthesize the waveform using FM synthesis with ADSR envelope modulation.
const vector<float> &SenoFM::synthesize()
{
    if (not adsr.active())
    {
        x.assign(x.size(), 0);
        bActive = false;
        return x;
    }
    else if (not bActive)
        return x;

    unsigned int index_floor, next_index; // Interpolation indexes
    float weight, weight_fm;              // Interpolation weights
    int index_floor_fm, next_index_fm;    // Frequency interpolation indexes
    std::vector<float> I_array(x.size()); // Array for modulation index I

    // Initialize I_array with user-input modulation index (constant)
    for (unsigned int i = 0; i < x.size(); i++)
    {
        I_array[i] = I2;
        // Apply exponential envelope if selected
        if (envelope > 0)
            I_array[i] = I_array[i] * pow(envelope, decay_count_I);
    }

    // Fill temp with one period of the new signal
    for (unsigned int i = 0; i < (unsigned int)note_int; ++i)
    {

        // Check if floating point index is out of bounds
        if ((long unsigned int)floor(index) > waveform_table.size() - 1)
            index = index - floor(index);

        // Obtain integer index
        index_floor = (int)floor(index);
        weight = index - index_floor;

        // Adjust interpolation indexes if necessary
        if (index_floor == (unsigned int)N - 1)
        {
            next_index = 0;
            index_floor = N - 1;
        }
        else
        {
            next_index = index_floor + 1;
        }
        // Interpolate table values
        temp[i] = ((1 - weight) * waveform_table[index_floor] + (weight)*waveform_table[next_index]);
        // Update real index
        index = index + index_step;
    }

    // Modulate the signal
    for (unsigned int i = 0; i < x.size(); ++i)
    {
        // Check if floating point index is out of bounds
        if (index_sensitivity < 0)
        {
            index_sensitivity = N_notes + index_sensitivity;
        }
        if ((int)floor(index_sensitivity) > note_int - 1)
        {

            index_sensitivity = index_sensitivity - (note_int - 1);
        }
        // Obtain integer index
        index_floor_fm = floor(index_sensitivity);
        weight_fm = index_sensitivity - index_floor_fm;

        // Adjust interpolation indexes if necessary
        if (index_floor_fm == note_int - 1)
        {
            next_index_fm = 0;
            index_floor_fm = note_int - 1;
        }
        else
        {
            next_index_fm = index_floor_fm + 1;
        }
        // Interpolate table values
        x[i] = A * ((1 - weight_fm) * temp[index_floor_fm] + weight_fm * (temp[next_index_fm]));

        // Update real index (phase) and modulated phase
        index_sensitivity = index_sensitivity + 1 - I_array[i] * sin(modulation_phase);
        modulation_phase = modulation_phase + phase_step_size;
    }

    while (modulation_phase > M_PI)
        modulation_phase -= 2 * M_PI;

    // Apply exponential or ADSR envelope modulation
    for (unsigned int i = 0; i < x.size(); i++)
    {
        if (envelope != 0)
        {
            if (envelope > 0) // Exponential decay based on 'envelope'
            {
                x[i] = x[i] * pow(envelope, decay_count);
                decay_count++;
            }
            else if (adsr.active() && envelope == -1)
            {
                x[i] = x[i] * adsr_s; // Adjust level to prevent attack overshoot
            }
        }
    }
    if (envelope <= 0)
        adsr(x); // Apply envelope to x and update ADSR internal state
    return x;
}
