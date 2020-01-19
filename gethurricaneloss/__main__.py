import logging
import click
from typing import Any
from gethurricaneloss import __version__ as app_version
import loss_framework


def print_version(ctx: Any, param: Any, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo("gethurricaneloss=={}".format(app_version))
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('-n', '--num_monte_carlo_samples', default=100, help='Number of simulation years.', type=int)
@click.option('-v/-i', '--verbose/--info', default=False, help='Enables debug logging.')
@click.option('-m/-s', '--multicpu/--singlecpu', default=False, help='Enables use of multipe CPUs.')
@click.argument('florida_landfall_rate', nargs=1, type=int)
@click.argument('florida_mean', nargs=1, type=float)
@click.argument('florida_stddev', nargs=1, type=float)
@click.argument('gulf_landfall_rate', nargs=1, type=int)
@click.argument('gulf_mean', nargs=1, type=float)
@click.argument('gulf_stddev', nargs=1, type=float)
def main(num_monte_carlo_samples: int, verbose: bool, multicpu: bool,
         florida_landfall_rate: int, florida_mean: float, florida_stddev: float,
         gulf_landfall_rate: int, gulf_mean: float, gulf_stddev: float) -> int:
    """
    The main function for the 'gethurricaneloss' application.

    Responsibility - to unpack any command line arguments, consturct the regions and the model
    then pass them into the loss-framework's calculator to calculate the total loss.
    """
    result = gethurricaneloss(num_monte_carlo_samples, verbose, multicpu,
                              florida_landfall_rate, florida_mean, florida_stddev,
                              gulf_landfall_rate, gulf_mean, gulf_stddev)
    print("Mean loss={} per year calculated over {} years.".format(result / num_monte_carlo_samples, num_monte_carlo_samples))
    return 0


def gethurricaneloss(num_monte_carlo_samples: int, verbose: bool, multicpu: bool,
                     florida_landfall_rate: int, florida_mean: float, florida_stddev: float,
                     gulf_landfall_rate: int, gulf_mean: float, gulf_stddev: float) -> float:

    return loss_framework.calculate_loss(num_monte_carlo_samples,
                                         florida_landfall_rate, florida_mean, florida_stddev,
                                         gulf_landfall_rate, gulf_mean, gulf_stddev)


def create_logger(log_level: int) -> logging.Logger:
    log = logging.getLogger("gethurricaneloss")
    ch = logging.StreamHandler()
    log.addHandler(ch)
    log.setLevel(log_level)
    return log


if __name__ == '__main__':
    main()
