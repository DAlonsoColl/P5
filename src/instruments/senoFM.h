#ifndef SENO_FM
#define SENO_FM

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc
{
  // Class SenoFM inherits from Instrument and implements FM synthesis with sine waves.
  class SenoFM : public upc::Instrument
  {
    EnvelopeADSR adsr; // ADSR envelope generator
    float index, N1, N2, envelope; // Parameters for frequency modulation
    int N, decay_count, decay_count_I, note_int; // Various counters and settings
    float A, index_step, index_sensitivity, N_notes, adsr_s, adsr_a, adsr_r, adsr_d; // Additional parameters
    std::vector<float> waveform_table, temp; // Tables for waveform and temporary storage
    long double modulation_phase, phase_step_size; // Phases for modulation
    float fm_modulation, I1, I2; // Frequency modulation parameters

  public:
    // Constructor that initializes parameters based on optional input 'param'.
    SenoFM(const std::string &param = "");

    // Process commands to start, sustain, or release a note.
    void command(long cmd, long note, long velocity = 1);

    // Synthesize and return a vector of float samples.
    const std::vector<float> &synthesize();

    // Check if the instrument is currently active.
    bool is_active() const { return bActive; }
  };
}

#endif
