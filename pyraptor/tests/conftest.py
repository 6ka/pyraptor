"""conftest"""

import pytest
import pandas as pd
import numpy as np

from pyraptor.model.structures import Timetable
from pyraptor.tests.utils import to_stops_and_trips, to_timetable


@pytest.fixture(scope="session")
def default_timetable() -> Timetable:
    """Default timetable"""
    df = get_default_data()
    stops, stop_times, trips = to_stops_and_trips(df)
    timetable_ = to_timetable(stops, stop_times, trips)
    return timetable_


@pytest.fixture(scope="session")
def timetable_with_transfers_and_fares() -> Timetable:
    """Timetable with fares"""
    stops, stop_times, trips = get_stop_times_with_transfers_and_fare()
    timetable_ = to_timetable(stops, stop_times, trips)
    return timetable_


@pytest.fixture(scope="session")
def timetable_with_many_transfers() -> Timetable:
    """Timetable with fares"""
    stops, stop_times, trips = get_stop_times_with_many_transfers()
    timetable_ = to_timetable(stops, stop_times, trips)
    return timetable_


def get_default_data():
    """Get default data for timetable"""

    def data_with_offset(trip_offset, time_offset):
        return [
            # First trip
            [
                trip_offset + 101,
                "A",
                time_offset + 100,
                "0",
                1,
                0,
            ],
            [
                trip_offset + 101,
                "C",
                time_offset + 600,
                "1",
                2,
                0,
            ],
            # Second trip
            [
                trip_offset + 202,
                "C",
                time_offset + 660,
                "2",
                1,
                0,
            ],
            [
                trip_offset + 202,
                "F",
                time_offset + 1500,
                "0",
                2,
                0,
            ],
            # Third trip
            [
                trip_offset + 303,
                "C",
                time_offset + 900,
                "2",
                1,
                0,
            ],
            [
                trip_offset + 303,
                "X",
                time_offset + 1200,
                "0",
                2,
                0,
            ],
            [
                trip_offset + 303,
                "F",
                time_offset + 1800,
                "0",
                2,
                0,
            ],
        ]

    data = data_with_offset(trip_offset=0, time_offset=0) + data_with_offset(
        trip_offset=10, time_offset=3600
    )
    df = pd.DataFrame(
        data,
        columns=[
            "treinnummer",
            "code",
            "vertrekmoment",
            "spoor",
            "vervoerstrajectindex",
            "toeslag",
        ],
    )
    df["aankomstmoment"] = df["vertrekmoment"]
    return df


def get_stop_times_with_transfers_and_fare():
    """Create timetable with transfers and fares"""

    stops = pd.DataFrame(
        {
            "stop_uic": [
                f"{i+8400000}"
                for i in [1]
                + [2] * 3
                + [3]
                + [4] * 3
                + [5, 6]
                + [7] * 2
                + [8] * 2
                + [9]
            ],
            "stop_id": [
                "st1_sp1",
                "st2_sp1",
                "st2_sp2",
                "st2_sp3",
                "st3_sp1",
                "st4_sp1",
                "st4_sp2",
                "st4_sp3",
                "st5_sp1",
                "st6_sp1",
                "st7_sp1",
                "st7_sp2",
                "st8_sp1",
                "st8_sp2",
                "st9_sp1",
            ],
        }
    )
    stops["parent_stop_id"] = stops["stop_id"].apply(lambda x: x[:-4])

    trip1 = pd.DataFrame(
        {
            "treinnummer": [101] * 5,
            "toeslag": [0] * 5,
            "stop_id": ["st1_sp1", "st2_sp2", "st3_sp1", "st4_sp2", "st5_sp1"],
            "vertrekmoment": range(1, 6),
            "vervoerstrajectindex": range(1, 6),
            "trip_id": [1] * 5,
        }
    )
    trip2 = pd.DataFrame(
        {
            "treinnummer": [203] * 4,
            "toeslag": [0] * 4,
            "stop_id": ["st8_sp1", "st7_sp1", "st4_sp3", "st6_sp1"],
            "vertrekmoment": np.arange(2.75, 4.75, 0.5),
            "vervoerstrajectindex": range(1, 5),
            "trip_id": [2] * 4,
        }
    )
    trip5 = pd.DataFrame(
        {
            "treinnummer": [201] * 4,
            "toeslag": [0] * 4,
            "stop_id": ["st8_sp1", "st7_sp1", "st4_sp3", "st6_sp1"],
            "vertrekmoment": np.arange(2.5, 4.5, 0.5),
            "vervoerstrajectindex": range(1, 5),
            "trip_id": [5] * 4,
        }
    )
    trip3 = pd.DataFrame(
        {
            "treinnummer": [301] * 2,
            "toeslag": [0] * 2,
            "stop_id": ["st2_sp3", "st7_sp2"],
            "vertrekmoment": [2, 3],
            "vervoerstrajectindex": range(1, 3),
            "trip_id": [3] * 2,
        }
    )
    trip4 = pd.DataFrame(
        {
            "treinnummer": [401] * 3,
            "toeslag": [0, 7, 0],
            "stop_id": ["st2_sp1", "st9_sp1", "st4_sp1"],
            "vertrekmoment": [2, 2.5, 3],
            "vervoerstrajectindex": range(1, 4),
            "trip_id": [4] * 3,
        }
    )
    trip6 = pd.DataFrame(
        {
            "treinnummer": [501] * 2,
            "toeslag": [0, 0],
            "stop_id": ["st2_sp2", "st8_sp2"],
            "vertrekmoment": [2, 2.5],
            "vervoerstrajectindex": range(1, 3),
            "trip_id": [6] * 2,
        }
    )
    trip7 = pd.DataFrame(
        {
            "treinnummer": [503] * 2,
            "toeslag": [0, 0],
            "stop_id": ["st2_sp2", "st8_sp2"],
            "vertrekmoment": [2.5, 3],
            "vervoerstrajectindex": range(1, 3),
            "trip_id": [7] * 2,
        }
    )

    stop_times = pd.concat(
        [trip1, trip2, trip3, trip4, trip5, trip6, trip7], axis=0, ignore_index=True
    )
    stop_times["vertrekmoment"] *= 600
    stop_times["aankomstmoment"] = stop_times["vertrekmoment"]
    trips = stop_times[["treinnummer", "trip_id", "toeslag"]].drop_duplicates()

    return stops, stop_times, trips


def get_stop_times_with_many_transfers():
    """Create timetable where it is possible to reach destination faster with many transfers"""

    stops = pd.DataFrame(
        {
            "stop_uic": [
                f"{i+8400000}"
                for i in [4] * 2
                + [5, 6]
                + [7] * 2
                + [8] * 2
                + [9]
                + [10]
                + [11]
                + [12]
                + [14]
            ],
            "stop_id": [
                "st4_sp1",
                "st4_sp2",
                "st5_sp1",
                "st6_sp1",
                "st7_sp1",
                "st7_sp2",
                "st8_sp1",
                "st8_sp2",
                "st9_sp1",
                "st10_sp1",
                "st11_sp1",
                "st12_sp1",
                "st14_sp1",
            ],
        }
    )
    stops["parent_stop_id"] = stops["stop_id"].apply(lambda x: x[:-4])

    trip1 = pd.DataFrame(
        {
            "treinnummer": [101] * 4,
            "toeslag": [0] * 4,
            "stop_id": ["st4_sp1", "st5_sp1", "st6_sp1", "st7_sp1"],
            "vertrekmoment": range(4, 17, 4),
            "vervoerstrajectindex": range(1, 5),
            "trip_id": [1] * 4,
        }
    )
    trip3 = pd.DataFrame(
        {
            "treinnummer": [301] * 3,
            "toeslag": [0] * 3,
            "stop_id": ["st9_sp1", "st5_sp1", "st10_sp1"],
            "vertrekmoment": range(8, 11),
            "vervoerstrajectindex": range(1, 4),
            "trip_id": [3] * 3,
        }
    )
    trip4 = pd.DataFrame(
        {
            "treinnummer": [401] * 3,
            "toeslag": [0] * 3,
            "stop_id": ["st10_sp1", "st11_sp1", "st12_sp1"],
            "vertrekmoment": range(11, 14),
            "vervoerstrajectindex": range(1, 4),
            "trip_id": [4] * 3,
        }
    )
    trip5 = pd.DataFrame(
        {
            "treinnummer": [501] * 2,
            "toeslag": [0] * 2,
            "stop_id": ["st12_sp1", "st7_sp1"],
            "vertrekmoment": range(14, 16),
            "vervoerstrajectindex": range(1, 3),
            "trip_id": [5] * 2,
        }
    )
    trip7 = pd.DataFrame(
        {
            "treinnummer": [701] * 3,
            "toeslag": [0] * 3,
            "stop_id": ["st10_sp1", "st7_sp1", "st14_sp1"],
            "vertrekmoment": range(16, 19),
            "vervoerstrajectindex": range(1, 4),
            "trip_id": [7] * 3,
        }
    )

    stop_times = pd.concat(
        [trip1, trip3, trip4, trip5, trip7], axis=0, ignore_index=True
    )
    stop_times["vertrekmoment"] *= 3600
    stop_times["aankomstmoment"] = stop_times["vertrekmoment"]
    trips = stop_times[["treinnummer", "trip_id", "toeslag"]].drop_duplicates()

    return stops, stop_times, trips
