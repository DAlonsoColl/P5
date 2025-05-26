#include <iostream>
#include <math.h>
#include "senoFM.h"
#include "keyvalue.h"
#include "wavfile_mono.h"

#include <stdlib.h>

using namespace upc;
using namespace std;


SenoFM::SenoFM(const std::string &param)
    : adsr(SamplingRate, param)
{
    bActive = false;
    x.resize(BSIZE);

    KeyValue kv(param);

    if (!kv.to_int("N", N))
        N = 40;

    if (!kv.to_float("ADSR_A", adsr_a))
        adsr_a = 0.1;

    if (!kv.to_float("ADSR_D", adsr_d))
        adsr_d = 0.05;

    if (!kv.to_float("ADSR_S", adsr_s))
        adsr_s = 0.5;

    if (!kv.to_float("ADSR_R", adsr_r))
        adsr_r = 0.1;

    if (!kv.to_float("I1", I1))
        I1 = 1;

    if (!kv.to_float("N1", N1))
        N1 = 1;

    if (!kv.to_float("N2", N2))
        N2 = 1;

    if (!kv.to_float("envelope", envelope))
        envelope = 0;

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
void SenoFM::command(long cmd, long note, long vel)
{
    if (cmd == 9)
    { 
        bActive = true;
        adsr.start();
        float f0note = pow(2, ((float)note - 69) / 12) * 440; 
        N_notes = 1 / f0note * SamplingRate;                   
        index_step = (float)N / N_notes;                        
        index = 0;
        index_sensitivity = 0;
        modulation_phase = 0;
        decay_count = 0;
        decay_count_I = 0;
        fm_modulation = f0note * N2 / N1;                         
        phase_step_size = 2 * M_PI * fm_modulation / SamplingRate; 
        note_int = round(N_notes);
        temp.resize(note_int);

        if (vel > 127)
            vel = 127;

        A = vel / 127.;
    }
    else if (cmd == 8)
    { 
        adsr.stop();
    }
    else if (cmd == 0)
    {
       
        adsr.set(adsr_s, adsr_a, adsr_d, adsr_r / 4, 1.5F);
        adsr.stop();
    }
}

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

    unsigned int index_floor, next_index; 
    float weight, weight_fm;            
    int index_floor_fm, next_index_fm;    
    std::vector<float> I_array(x.size()); 

    
    for (unsigned int i = 0; i < x.size(); i++)
    {
        I_array[i] = I2;
        
        if (envelope > 0)
            I_array[i] = I_array[i] * pow(envelope, decay_count_I);
    }

  
    for (unsigned int i = 0; i < (unsigned int)note_int; ++i)
    {

       
        if ((long unsigned int)floor(index) > waveform_table.size() - 1)
            index = index - floor(index);

        
        index_floor = (int)floor(index);
        weight = index - index_floor;

       
        if (index_floor == (unsigned int)N - 1)
        {
            next_index = 0;
            index_floor = N - 1;
        }
        else
        {
            next_index = index_floor + 1;
        }
        
        temp[i] = ((1 - weight) * waveform_table[index_floor] + (weight)*waveform_table[next_index]);
        
        index = index + index_step;
    }

   
    for (unsigned int i = 0; i < x.size(); ++i)
    {
        
        if (index_sensitivity < 0)
        {
            index_sensitivity = N_notes + index_sensitivity;
        }
        if ((int)floor(index_sensitivity) > note_int - 1)
        {

            index_sensitivity = index_sensitivity - (note_int - 1);
        }
       
        index_floor_fm = floor(index_sensitivity);
        weight_fm = index_sensitivity - index_floor_fm;

        
        if (index_floor_fm == note_int - 1)
        {
            next_index_fm = 0;
            index_floor_fm = note_int - 1;
        }
        else
        {
            next_index_fm = index_floor_fm + 1;
        }
        
        x[i] = A * ((1 - weight_fm) * temp[index_floor_fm] + weight_fm * (temp[next_index_fm]));

        
        index_sensitivity = index_sensitivity + 1 - I_array[i] * sin(modulation_phase);
        modulation_phase = modulation_phase + phase_step_size;
    }

    while (modulation_phase > M_PI)
        modulation_phase -= 2 * M_PI;

    
    for (unsigned int i = 0; i < x.size(); i++)
    {
        if (envelope != 0)
        {
            if (envelope > 0) 
            {
                x[i] = x[i] * pow(envelope, decay_count);
                decay_count++;
            }
            else if (adsr.active() && envelope == -1)
            {
                x[i] = x[i] * adsr_s; 
            }
        }
    }
    if (envelope <= 0)
        adsr(x); 
    return x;
}
