import hashlib
from math import log2
import random
import matplotlib.pyplot as plt


def apply_mask(data, mask):
    return [format(int(val, 2) & int(mask, 2), '08b') for val in data]


def xor_and_update_mask(data_one, data_two, mask):
    # Apply the mask to both captures
    masked_data_one = apply_mask(data_one, mask)
    masked_data_two = apply_mask(data_two, mask)

    # XOR the masked values to find differing bits
    xor_result = [format(int(val1, 2) ^ int(val2, 2), '08b')
                  for val1, val2 in zip(masked_data_one, masked_data_two)]

    # Update the mask with newly found flipping bits
    updated_mask = ''.join(
        ['1' if bit == '1' else '0' for bit in ''.join(xor_result)])

    return xor_result, updated_mask


def compute_key(ram_buffer, mask):
    tmp = [ram_byte & mask_byte for ram_byte,
           mask_byte in zip(ram_buffer, mask)]
    tmp_bytes = bytes(tmp)

    sha256_hash = hashlib.sha256(tmp_bytes).digest()
    return sha256_hash


def hamming_distance(id1, id2):
    # Calculate Hamming distance between two binary strings
    return sum(bit1 != bit2 for bit1, bit2 in zip(id1, id2))


def calculate_ubase(response_ids):
    n = len(response_ids)
    total_ubase = 0

    if n > 1:
        for i in range(n - 1):
            for j in range(i + 1, n):
                hd = hamming_distance(response_ids[i], response_ids[j])
                ubase = hd / len(response_ids[i])
                total_ubase += ubase
                print(f"Hamming distance for pair {i+1}-{j+1}: {hd}")

                # Print uniqueness for each pair
                print(f"Uniqueness for pair {i+1}-{j+1}: {ubase * 100}")

        return total_ubase * (2 / (n * (n - 1)))
    else:
        # Return 0 if there's only one response identifier
        return 0


def calculate_mu(response_ids):
    k = len(response_ids)
    total_mu = 0

    for i in range(k):
        total_mu += calculate_ubase(response_ids[i:]) / \
            (k - i) if (k - i) > 0 else 1

    return total_mu / k


def calculate_diffuseness(response_bitstrings):
    K = len(response_bitstrings)
    L = len(response_bitstrings[0])

    diffusion_sum = 0

    for l in range(L):
        for i in range(K - 1):
            for j in range(i + 1, K):
                bit_i = int(response_bitstrings[i][l])
                bit_j = int(response_bitstrings[j][l])
                diffusion_sum += bit_i ^ bit_j

    diffusion = (4 / (K**2 * L)) * diffusion_sum
    return diffusion


def calculate_reliability(response_bitstrings, Na):
    Nc = len(response_bitstrings)
    reliability_sum = 0

    for k in range(Nc):
        sum_bk_j = sum(int(response_bitstrings[k][j]) / Na for j in range(Na))
        reliability_sum += log2(max(sum_bk_j, 1 - sum_bk_j))

    reliability = 1 + (1 / Nc) * reliability_sum
    return reliability


# Example usage with your provided data
data_one = [
    "10110011", "00001000", "10011110", "10111100", "00011001", "00001100", "11011100", "11101101",
    "01010101", "01011100", "11001100", "01010101", "00110101", "00100000", "10011000", "11001001",
    "00010100", "01111000", "00101000", "01110111", "01111111", "01100111", "00010101", "01010010",
    "00010011", "11010000", "10110011", "00101101", "00101010", "00110110", "00110010", "10111010",
    "10011000", "10000110", "10011010", "10101111", "00010100", "11100010", "01011011", "00001101",
    "11010101", "00100110", "01001011", "11011001", "11011000", "10101111", "11111001", "11001000",
    "01011001", "00111110", "10101011", "11010010", "00011101", "11111101", "01001101", "11000010",
    "11010101", "01000001", "01111100", "00010100", "10011011", "01111001", "11101101", "00101111"
]

data_two = [
    "10110011", "00001000", "11111110", "10111100", "00001001", "11001100", "11011100", "11000001",
    "01010101", "01010100", "11101101", "01010100", "00110101", "00100000", "10011010", "11001001",
    "00011100", "01111000", "00101000", "01110011", "01111111", "01100111", "00010101", "01100010",
    "00010011", "11010000", "10110011", "00101101", "00100000", "00110110", "00100000", "10101010",
    "10011000", "10000010", "10011010", "10101111", "00010000", "01000010", "01011011", "00001101",
    "11010101", "00101110", "01101001", "11011001", "11011000", "10101111", "11111001", "11001000",
    "01011101", "00111110", "10101011", "11010010", "00011101", "11111101", "01001101", "11000010",
    "11010101", "01100001", "01111100", "00010100", "10001011", "01011001", "11111101", "00101011"
]

current_mask = "11111111"

xor_result, updated_mask = xor_and_update_mask(
    data_one, data_two, current_mask)

print("XOR Result:")
print(xor_result)
print("\nUpdated Mask:")
print(updated_mask)


# Calculate uniqueness (U_base) for each pair of response identifiers
response_identifiers = [data_one, data_two]
ubase_values = []

for i in range(len(response_identifiers)):
    for j in range(i + 1, len(response_identifiers)):
        ubase = calculate_ubase(
            [response_identifiers[i], response_identifiers[j]])
        ubase_values.append(ubase)

# Average uniqueness (MU)
mu_value = calculate_mu(ubase_values)

print(f"\nAverage Uniqueness (MU): {mu_value}")


def calculate_entropy(data):
    total_bits = len(data)
    ones_frequency = sum(int(bit) for bit in data) / total_bits
    entropy = - sum(p * log2(p) if p !=
                    0 else 0 for p in [ones_frequency, 1 - ones_frequency])
    return entropy * 100


# Combine the XOR result into a single string
data_combined = ''.join(xor_result)

# Calculate entropy (randomness) of the combined XOR result
entropy = calculate_entropy(data_combined)
print("\nEntropy (Randomness):", entropy)

# Convert data and mask to bytes
data_one_bytes = [int(val, 2) for val in data_one]
data_two_bytes = [int(val, 2) for val in data_two]
mask_bytes = bytes([int(bit, 2) for bit in updated_mask])


# Apply the updated mask and calculate the SHA-256 hash
key_one = compute_key(data_one_bytes, mask_bytes)
key_two = compute_key(data_two_bytes, mask_bytes)

print("\nPrivate Key One:", key_one.hex())
print("Private Key Two:", key_two.hex())


# Example usage with your provided data
response_bitstrings = [data_one, data_two]
diffuseness_value = calculate_diffuseness(response_bitstrings)
print("Diffuseness Value:", diffuseness_value)

response_bitstrings = [data_one, data_two]
Na = len(data_one[0])  # Assuming all responses have the same length
reliability_value = calculate_reliability(response_bitstrings, Na)
print("Reliability Value:", reliability_value)


def plot_metrics(mu_value, entropy, diffuseness_value, reliability_value):
    metrics = ['Uniqueness (MU)', 'Entropy', 'Diffuseness', 'Reliability']
    values = [mu_value * 100, entropy, diffuseness_value, reliability_value]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    fig.suptitle('PUF Metrics Analysis', fontsize=16)

    for i, (metric, value) in enumerate(zip(metrics, values)):
        row, col = i // 2, i % 2
        axes[row, col].bar([metric], [value], color=[
                           'blue', 'orange', 'green', 'red'])
        axes[row, col].set_title(metric)
        axes[row, col].set_ylabel('Value')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    plot_metrics(mu_value, entropy, diffuseness_value, reliability_value)


def generate_challenge(length):
    # Generate a random challenge of the specified length
    return [random.choice(['0', '1']) for _ in range(length)]


def send_challenge_to_puf(challenge, puf_code):
    # In a real scenario, this is where you'd communicate with the PUF hardware
    # Here, we'll use the existing PUF code to get a response
    response, _ = xor_and_update_mask(data_one, data_two, ''.join(challenge))
    return response


def main():
    # Assuming the PUF challenge length is the same as the original data length
    challenge_length = len(data_one[0])

    # Generate a challenge
    challenge = generate_challenge(challenge_length)

    print("Challenge:", ''.join(challenge))

    # Send the challenge to the PUF
    response = send_challenge_to_puf(challenge, xor_and_update_mask)

    print("Response:", ''.join(response))

    # Continue with the rest of your analysis if needed


if __name__ == "__main__":
    main()
