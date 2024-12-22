import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse
from typing import Optional

"""
Data Plotting Tool for Solar, Battery, and RSSI Data

This script reads data from a specified input file, processes it into a pandas DataFrame, and then generates plots of specific columns over time.
It supports visualizations of the following data:
- Solar voltage ('SOLAR') vs Time
- Battery voltage ('BATT1') vs Time
- RSSI values ('rssi') vs Time

The user can specify the number of days for which the plots are generated using the `-n` flag. The data file must be in a format where each line 
represents a dictionary-like entry containing keys such as 'time', 'SOLAR', 'BATT1', and 'rssi'.

Usage:
    python plot_data.py <file_path> [-n <num_days>]

Arguments:
    <file_path>      : Path to the input data file (required).
    -n <num_days>    : Number of days to plot. Default is 7 days if not specified.

Example:
    python plot_data.py data.txt -n 30
    This will plot the 'SOLAR' and 'BATT1' columns vs time for the last 30 days from 'data.txt'.

Dependencies:
    - pandas: For data processing and manipulation.
    - matplotlib: For generating plots.
    - argparse: For handling command-line arguments.

File Format:
    The input data file should contain lines that are dictionary-like strings with at least the following keys:
    - 'time': A string representing the timestamp, e.g., "12/25/2023, 14:30:00".
    - 'SOLAR': Solar voltage value (float or int).
    - 'BATT1': Battery voltage value (float or int).
    - 'rssi': RSSI value (float or int, optional).

    Example line:
        {'time': '12/25/2023, 14:30:00', 'SOLAR': 3.45, 'BATT1': 4.12, 'rssi': -70.2}

This script assumes that the data file is correctly formatted and that the necessary columns exist in the input data.

"""

def create_dataframe(file_path: str) -> pd.DataFrame:
    """
    Reads data from a file and creates a pandas DataFrame.
    Safely parses each line and fixes any known issues (e.g., typos in keys).

    :param file_path: The path to the data file.
    :return: A pandas DataFrame containing the parsed data.
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                # Safely parse the line as a dictionary
                entry = eval(line.strip(), {"__builtins__": None})  # Avoid unsafe eval
                # Fix the typo in the key if it exists
                if 'SOLA(1)R' in entry:
                    entry['SOLAR'] = entry.pop('SOLA(1)R')
                data.append(entry)
            except Exception as e:
                print(f"Error processing line: {line} \nError: {e}")
                continue  # Skip problematic lines

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)

    # Convert 'time' field to datetime objects
    df['time'] = pd.to_datetime(df['time'], format="%m/%d/%Y, %H:%M:%S")

    return df


def plot_data(df: pd.DataFrame, num_days: int, columns: list[str], colors: list[str], title: str, ylabel: str) -> None:
    """
    Helper function to plot specified columns against time for the last 'num_days' days.

    :param df: The DataFrame containing the data.
    :param num_days: The number of days for the plot.
    :param columns: List of column names to plot.
    :param colors: List of colors for each plot.
    :param title: The title of the plot.
    :param ylabel: The label for the y-axis.
    :return: None
    """
    # Get the current date and calculate the date 'num_days' ago
    current_date = datetime.now()
    days_ago = current_date - timedelta(days=num_days)

    # Filter the DataFrame for data within the last 'num_days'
    df_filtered = df[df['time'] >= days_ago]

    plt.figure(figsize=(10, 6))

    # Plot each column
    for col, color in zip(columns, colors):
        if col in df_filtered:
            plt.plot(df_filtered['time'], df_filtered[col], linestyle='-', color=color, label=col)
        else:
            print(f"Column '{col}' not found in the DataFrame.")
            continue

    # Adding labels and title
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.title(f'{title} (Last {num_days} Days)')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display grid and legend
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_solar_and_batt1_for_days(df: pd.DataFrame, num_days: int) -> None:
    """
    Plots the 'SOLAR' and 'BATT1' columns vs 'time' for the last 'num_days' days.

    :param df: The DataFrame containing the data.
    :param num_days: The number of days for the plot.
    :return: None
    """
    plot_data(
        df,
        num_days,
        columns=['SOLAR', 'BATT1'],
        colors=['red', 'blue'],
        title='Solar and Battery Voltage vs Time',
        ylabel='Voltage (V)'
    )


def plot_rssi_vs_time(df: pd.DataFrame, num_days: int) -> None:
    """
    Plots the 'rssi' column vs 'time' for the last 'num_days' days.

    :param df: The DataFrame containing the data.
    :param num_days: The number of days for the plot.
    :return: None
    """
    plot_data(
        df,
        num_days,
        columns=['rssi'],
        colors=['green'],
        title='RSSI vs Time',
        ylabel='RSSI (dBm)'
    )


def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments using argparse.

    :return: Parsed arguments as a Namespace object.
    """
    parser = argparse.ArgumentParser(
        description="Process a data file and plot SOLAR, BATT1, and RSSI over time."
    )

    # Positional argument for file path
    parser.add_argument(
        'file_path',
        type=str,
        help="Path to the input data file."
    )

    # Optional argument for num_days, default is 7
    parser.add_argument(
        '-n', '--num_days',
        type=int,
        default=7,
        help="Number of days to plot (default is 7)."
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Parse the arguments from the command line
    args = parse_args()

    # Step 1: Create the DataFrame from the file
    df = create_dataframe(args.file_path)

    # Step 2: Plot SOLAR and BATT1 vs. TIME for the last 'num_days' days (e.g., 7 days)
    plot_solar_and_batt1_for_days(df, args.num_days)

    # Step 3: Plot RSSI vs TIME for the last 'num_days' days (e.g., 7 days)
    plot_rssi_vs_time(df, args.num_days)
