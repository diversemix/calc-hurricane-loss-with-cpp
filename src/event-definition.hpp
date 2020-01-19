#include <random>

#ifndef _EVENT_DEF_HPP
#define _EVENT_DEF_HPP

class EventDefinition {
  public:
    EventDefinition(double rate, double mean, double stddev ) {
      this->initialise(rate, mean, stddev);
    }

    EventDefinition(const EventDefinition & right) {
      this->initialise(right.event_rate, right.loss_mean, right.loss_stddev);
    }

    double loss_in_year() {

      double total = 0;
      int num_events = this->event_distribution(this->generator);
      for (int i = 0; i < num_events; i++)
      {
        total += this->loss_distribution(this->generator);
      }

      return total;
    }

  private:
    void initialise(double rate, double mean, double stddev) {
      this->event_rate = rate;
      this->loss_mean = mean;
      this->loss_stddev = stddev;

      this->event_distribution = std::poisson_distribution<>(this->event_rate);
      this->loss_distribution = std::lognormal_distribution<>(this->loss_mean, this->loss_stddev);
      this->generator = std::mt19937(this->rd());
    }

    double event_rate;
    double loss_mean;
    double loss_stddev;
    std::random_device rd;

    // https://en.cppreference.com/w/cpp/numeric/random/poisson_distribution/poisson_distribution
    std::poisson_distribution<> event_distribution;
    std::lognormal_distribution<> loss_distribution;
    std::mt19937 generator;

};
#endif // _EVENT_DEF_HPP
