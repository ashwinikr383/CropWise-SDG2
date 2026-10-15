"""
CropWise - Synthetic Agricultural Dataset Generator
SDG 2: Zero Hunger | Sustainable Precision Agriculture

IMPORTANT NOTICE:
This script produces SYNTHETIC agricultural data designed for educational,
research, and machine learning prototyping purposes. It is NOT field-collected
empirical farm data and should not be used as the sole basis for real-world
farming or financial decisions without agronomist validation.
"""

import os
import argparse
import numpy as np
import pandas as pd

# Define agronomic parameter profiles for 22 crops
# Centroids (mean) and spread (standard deviation) for:
# N (kg/ha), P (kg/ha), K (kg/ha), Temperature (°C), Humidity (%), pH, Rainfall (mm)
CROP_PROFILES = {
    "rice": {
        "N": (80.0, 10.0), "P": (48.0, 7.0), "K": (40.0, 4.0),
        "temperature": (24.0, 2.5), "humidity": (82.5, 4.5),
        "ph": (6.4, 0.4), "rainfall": (235.0, 25.0)
    },
    "maize": {
        "N": (78.0, 11.0), "P": (48.0, 7.0), "K": (20.0, 3.0),
        "temperature": (22.5, 3.2), "humidity": (65.0, 6.0),
        "ph": (6.3, 0.4), "rainfall": (85.0, 15.0)
    },
    "chickpea": {
        "N": (40.0, 9.5), "P": (68.0, 7.0), "K": (80.0, 4.0),
        "temperature": (18.8, 1.8), "humidity": (16.8, 1.8),
        "ph": (7.3, 0.5), "rainfall": (80.0, 10.0)
    },
    "kidney beans": {
        "N": (21.0, 6.0), "P": (67.5, 7.0), "K": (20.0, 3.0),
        "temperature": (20.1, 2.5), "humidity": (21.5, 2.0),
        "ph": (5.7, 0.2), "rainfall": (105.0, 20.0)
    },
    "pigeon peas": {
        "N": (20.5, 6.0), "P": (67.5, 7.5), "K": (20.0, 3.0),
        "temperature": (27.7, 4.0), "humidity": (48.0, 9.0),
        "ph": (5.8, 0.5), "rainfall": (150.0, 28.0)
    },
    "moth beans": {
        "N": (21.5, 6.0), "P": (48.0, 6.5), "K": (20.0, 3.0),
        "temperature": (28.2, 2.5), "humidity": (53.0, 6.0),
        "ph": (6.8, 0.8), "rainfall": (51.0, 12.0)
    },
    "mung bean": {
        "N": (21.0, 6.0), "P": (47.5, 6.0), "K": (20.0, 3.0),
        "temperature": (28.5, 1.2), "humidity": (85.5, 3.0),
        "ph": (6.7, 0.3), "rainfall": (48.5, 6.5)
    },
    "black gram": {
        "N": (40.0, 7.0), "P": (67.5, 7.0), "K": (19.5, 3.0),
        "temperature": (30.0, 2.8), "humidity": (65.0, 3.0),
        "ph": (7.1, 0.4), "rainfall": (68.0, 4.5)
    },
    "lentil": {
        "N": (18.5, 5.5), "P": (68.0, 7.0), "K": (19.5, 3.0),
        "temperature": (24.5, 4.0), "humidity": (64.8, 3.5),
        "ph": (6.9, 0.5), "rainfall": (45.5, 5.5)
    },
    "pomegranate": {
        "N": (19.0, 6.0), "P": (19.0, 5.5), "K": (40.0, 3.5),
        "temperature": (21.8, 2.0), "humidity": (90.0, 3.0),
        "ph": (6.4, 0.4), "rainfall": (107.5, 3.5)
    },
    "banana": {
        "N": (100.5, 10.0), "P": (82.0, 8.0), "K": (50.0, 3.5),
        "temperature": (27.4, 1.8), "humidity": (80.3, 3.2),
        "ph": (5.9, 0.3), "rainfall": (104.5, 8.5)
    },
    "mango": {
        "N": (20.0, 6.0), "P": (27.0, 5.5), "K": (30.0, 3.5),
        "temperature": (31.2, 2.8), "humidity": (50.0, 3.2),
        "ph": (5.8, 0.5), "rainfall": (95.0, 6.5)
    },
    "grapes": {
        "N": (23.0, 6.5), "P": (132.5, 8.0), "K": (200.0, 3.5),
        "temperature": (23.8, 5.5), "humidity": (81.8, 2.0),
        "ph": (6.0, 0.3), "rainfall": (69.5, 3.0)
    },
    "watermelon": {
        "N": (99.5, 11.0), "P": (17.0, 5.0), "K": (50.0, 3.5),
        "temperature": (25.5, 1.5), "humidity": (85.1, 2.8),
        "ph": (6.5, 0.3), "rainfall": (50.8, 5.5)
    },
    "muskmelon": {
        "N": (100.0, 10.0), "P": (17.5, 5.0), "K": (50.0, 3.5),
        "temperature": (28.6, 1.2), "humidity": (92.3, 1.5),
        "ph": (6.4, 0.2), "rainfall": (24.7, 2.8)
    },
    "apple": {
        "N": (20.8, 6.0), "P": (134.0, 7.5), "K": (200.0, 3.5),
        "temperature": (22.6, 1.5), "humidity": (92.3, 1.5),
        "ph": (5.9, 0.3), "rainfall": (112.5, 7.5)
    },
    "orange": {
        "N": (19.8, 6.0), "P": (16.5, 5.0), "K": (10.0, 2.5),
        "temperature": (22.8, 4.5), "humidity": (92.1, 1.8),
        "ph": (7.0, 0.5), "rainfall": (110.0, 6.0)
    },
    "papaya": {
        "N": (49.8, 8.0), "P": (59.0, 6.5), "K": (50.0, 3.5),
        "temperature": (33.7, 4.0), "humidity": (92.4, 1.8),
        "ph": (6.7, 0.2), "rainfall": (142.5, 45.0)
    },
    "coconut": {
        "N": (22.0, 6.5), "P": (17.0, 5.0), "K": (30.0, 3.5),
        "temperature": (27.4, 1.2), "humidity": (94.8, 2.5),
        "ph": (5.9, 0.3), "rainfall": (175.5, 30.0)
    },
    "cotton": {
        "N": (117.8, 12.0), "P": (46.2, 7.0), "K": (19.5, 3.0),
        "temperature": (24.0, 1.5), "humidity": (79.8, 3.5),
        "ph": (6.9, 0.5), "rainfall": (80.3, 11.5)
    },
    "jute": {
        "N": (78.4, 11.0), "P": (46.8, 7.0), "K": (40.0, 3.5),
        "temperature": (24.9, 1.5), "humidity": (79.6, 3.8),
        "ph": (6.7, 0.4), "rainfall": (174.7, 18.0)
    },
    "coffee": {
        "N": (101.2, 11.5), "P": (28.7, 6.0), "K": (30.0, 3.5),
        "temperature": (25.5, 2.5), "humidity": (58.9, 7.5),
        "ph": (6.8, 0.4), "rainfall": (158.0, 26.0)
    }
}

# Physical bounding constraints
PARAM_BOUNDS = {
    "N": (0.0, 150.0),
    "P": (5.0, 150.0),
    "K": (5.0, 210.0),
    "temperature": (5.0, 50.0),
    "humidity": (10.0, 100.0),
    "ph": (3.5, 9.5),
    "rainfall": (10.0, 350.0)
}


def generate_dataset(samples_per_crop: int = 100, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate reproducible synthetic agricultural dataset across 22 crops.

    Parameters:
        samples_per_crop (int): Number of records per crop (default 100 -> 2,200 total).
        random_seed (int): Seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame containing 7 input features, crop label, and synthetic indicator.
    """
    np.random.seed(random_seed)
    records = []

    for crop_name, params in CROP_PROFILES.items():
        for _ in range(samples_per_crop):
            row = {}
            for feature, (mean, std) in params.items():
                min_val, max_val = PARAM_BOUNDS[feature]
                val = np.random.normal(loc=mean, scale=std)
                # Clip to realistic physical boundaries
                val = np.clip(val, min_val, max_val)
                # Round integers for N, P, K and 2 decimals for continuous values
                if feature in ["N", "P", "K"]:
                    row[feature] = int(round(val))
                elif feature == "ph":
                    row[feature] = round(float(val), 2)
                else:
                    row[feature] = round(float(val), 2)

            row["label"] = crop_name
            records.append(row)

    df = pd.DataFrame(records)
    # Shuffle dataset rows deterministically
    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic training data for CropWise (SDG 2 Zero Hunger)"
    )
    parser.add_argument(
        "--samples_per_crop",
        type=int,
        default=100,
        help="Number of samples to generate per crop (default: 100, total = 2200 records)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join("data", "crop_data.csv"),
        help="Target output CSV file path"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic generation"
    )

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    print("=" * 65)
    print("CropWise - Synthetic Agricultural Dataset Generator")
    print("SDG 2: Zero Hunger | Sustainable Precision Agriculture")
    print("=" * 65)
    print(f"[*] Configuration: {len(CROP_PROFILES)} crops | {args.samples_per_crop} samples/crop")
    print(f"[*] Seed: {args.seed}")
    print("[*] Generating synthetic data distributions...")

    df = generate_dataset(samples_per_crop=args.samples_per_crop, random_seed=args.seed)

    # Save to CSV
    df.to_csv(args.output, index=False)

    print(f"[+] Successfully generated {len(df)} synthetic records.")
    print(f"[+] Dataset saved to: {os.path.abspath(args.output)}")
    print("[!] NOTICE: All data is synthetic and clearly designated for prototype ML modeling.")
    print("=" * 65)


if __name__ == "__main__":
    main()

