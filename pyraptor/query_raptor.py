"""Run query with RAPTOR algorithm"""
import argparse

from loguru import logger

from pyraptor.dao.timetable import read_timetable
from pyraptor.model.structures import Journey, Timetable
from pyraptor.model.raptor import (
    RaptorAlgorithm,
    reconstruct_journey,
    best_stop_at_target_station,
)
from pyraptor.util import str2sec
import time


def parse_arguments():
    """Parse arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="data/output",
        help="Input directory",
    )
    parser.add_argument(
        "-or",
        "--origin",
        type=str,
        default="Hertogenbosch ('s)",
        help="Origin station of the journey",
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        default="Rotterdam Centraal",
        help="Destination station of the journey",
    )
    parser.add_argument(
        "-t", "--time", type=str, default="08:35:00", help="Departure time (hh:mm:ss)"
    )
    parser.add_argument(
        "-r",
        "--rounds",
        type=int,
        default=5,
        help="Number of rounds to execute the RAPTOR algorithm",
    )
    arguments = parser.parse_args()
    return arguments


def main(
    input_folder,
    origin_station,
    destination_station,
    departure_time,
    rounds,
):
    """Run RAPTOR algorithm"""

    logger.debug("Input directory     : {}", input_folder)
    logger.debug("Origin station      : {}", origin_station)
    logger.debug("Destination station : {}", destination_station)
    logger.debug("Departure time      : {}", departure_time)
    logger.debug("Rounds              : {}", str(rounds))

    timetable = read_timetable(input_folder)

    logger.info(f"Calculating network from: {origin_station}")

    # Departure time seconds
    dep_secs = str2sec(departure_time)
    logger.debug("Departure time (s.)  : " + str(dep_secs))

    # Find route between two stations
    start = time.time()
    journey_to_destinations = run_raptor(
        timetable,
        origin_station,
        destination_station,
        dep_secs,
        rounds,
    )
    end = time.time()

    # Print journey to destination
    journey_to_destinations.print(dep_secs=dep_secs)
    logger.debug("Found in {:.2f} s.".format(end - start))


def run_raptor(
    timetable: Timetable,
    origin_station: str,
    destination_station: str,
    dep_secs: int,
    rounds: int,
) -> Journey:
    """
    Run the Raptor algorithm.

    :param timetable: timetable
    :param origin_station: Name of origin station
    :param destination_station: Name of destination station
    :param dep_secs: Time of departure in seconds
    :param rounds: Number of iterations to perform
    """

    # Get stops for origin and all destinations
    from_stops = timetable.stations.get(origin_station).stops
    to_stops = timetable.stations.get(destination_station).stops

    # Run Round-Based Algorithm
    raptor = RaptorAlgorithm(timetable)
    best_labels = raptor.run(from_stops, timetable.stations[destination_station], dep_secs, rounds)


    # Determine the best journey to all possible destination stations
    dest_stop = best_stop_at_target_station(to_stops, best_labels)
    if dest_stop != 0:
        return reconstruct_journey(dest_stop, best_labels)


if __name__ == "__main__":
    args = parse_arguments()
    main(
        args.input,
        args.origin,
        args.destination,
        args.time,
        args.rounds,
    )
