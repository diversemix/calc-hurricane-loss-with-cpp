// poisson_distribution
#include <iostream>
#include <thread>
#include "event-definition.hpp"

int multi_calculator(int n_years, EventDefinition & florida, EventDefinition & gulf) {
  unsigned num_cpus = std::thread::hardware_concurrency();
  std::cout << "Launching " << num_cpus << " threads\n";

  std::vector<std::thread> threads(num_cpus);
  std::vector<double> results(num_cpus);

  const int new_years = int(n_years / num_cpus);
  for (unsigned i = 0; i < num_cpus; ++i) {

    threads[i] = std::thread([i, num_cpus, &results, new_years, florida, gulf] {
      EventDefinition newFlorida = EventDefinition(florida);
      EventDefinition newGulf = EventDefinition(gulf);
      double loss = 0;

      for (int i = 0; i < new_years; ++i) {
        loss += newFlorida.loss_in_year();
        loss += newGulf.loss_in_year();
      }

      results[i] = loss;
    });
  }

  for (auto& t : threads) {
    t.join();
  }

  double total_loss = 0;
  for (auto loss : results) {
    total_loss += loss;
  }

  return total_loss;
}


double single_calculator(int n_years, EventDefinition & florida, EventDefinition & gulf) {

  double total_loss = 0;

  for (int i = 0; i < n_years; ++i) {
    total_loss += florida.loss_in_year();
    total_loss += gulf.loss_in_year();
  }

  return total_loss;
}

double calculate_loss(int n_years,
  double florida_rate, double florida_mean, double florida_stddev,
  double gulf_rate, double gulf_mean, double gulf_stddev)
{

  EventDefinition florida = EventDefinition(florida_rate, florida_mean, florida_stddev);
  EventDefinition gulf = EventDefinition(gulf_rate, gulf_mean, gulf_stddev);

  double total_loss = 0;
  if (n_years > 10000)
    total_loss = multi_calculator(n_years, florida, gulf);
  else
    total_loss = single_calculator(n_years, florida, gulf);

  std::cout << "Mean loss=" << total_loss / n_years
            << " per year calculated over " << n_years << " years."
            << std::endl;


  return total_loss;
}

