import random
import time

WINDOW_SIZE = 4
LOSS_PROBABILITY = 0.2
ACK_LOSS_PROBABILITY = 0.2
TIMEOUT = 7
MAX_RETRANSMISSIONS = 5

# Simulated packet data
packets = [
    "Packet 1: Hello",
    "Packet 2: World",
    "Packet 3: This",
    "Packet 4: is",
    "Packet 5: a",
    "Packet 6: Go-Back-N",
    "Packet 7: ARQ",
    "Packet 8: Protocol"
]
NUM_PACKETS = len(packets)

def is_packet_lost():
    return random.random() < LOSS_PROBABILITY

def is_ack_lost():
    return random.random() < ACK_LOSS_PROBABILITY

def send_packet(packet_num, ack_received_for_packet, total_retransmissions):
    ack_received = False
    print(f"Sending packet {packet_num + 1}: {packets[packet_num]}")

    if is_packet_lost():
        print(f"Packet {packet_num + 1} is lost.")
        return

    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        if is_ack_lost():
            print(f"ACK for packet {packet_num + 1} is lost.")
            break
        else:
            ack_received = True
            print(f"ACK received for packet {packet_num + 1}.")
            break

    if ack_received:
        ack_received_for_packet[packet_num % WINDOW_SIZE] = 1
    else:
        print(f"Timeout for packet {packet_num + 1}, resending the window.")
        total_retransmissions[0] += 1

def go_back_n_arq_simulation():
    packet_num = 0
    total_packets_sent = 0
    total_retransmissions = [0]
    total_successful_packets = 0

    ack_received_for_packet = [0] * WINDOW_SIZE

    start_time = time.time()

    while packet_num < NUM_PACKETS:
        print(f"\n----- Sending Window: Packets {packet_num + 1} to {min(packet_num + WINDOW_SIZE, NUM_PACKETS)} -----")

        for i in range(packet_num, min(packet_num + WINDOW_SIZE, NUM_PACKETS)):
            send_packet(i, ack_received_for_packet, total_retransmissions)
            total_packets_sent += 1

        all_acks_received = all(ack_received_for_packet[i] == 1 for i in range(min(WINDOW_SIZE, NUM_PACKETS - packet_num)))

        if all_acks_received:
            print("All ACKs received for current window. Proceeding to next window.")
            total_successful_packets += min(WINDOW_SIZE, NUM_PACKETS - packet_num)
            packet_num += WINDOW_SIZE
        else:
            print("Some packets in the window were not acknowledged, retrying...")

        ack_received_for_packet = [0] * WINDOW_SIZE
        time.sleep(1)

    end_time = time.time()
    total_time_taken = end_time - start_time
    protocol_efficiency = (total_successful_packets / total_packets_sent) * 100 if total_packets_sent > 0 else 0
    throughput = total_successful_packets / total_time_taken if total_time_taken > 0 else 0

    print("\nTransmission Report:")
    print(f"Total packets sent: {total_packets_sent}")
    print(f"Total retransmissions: {total_retransmissions[0]}")
    print(f"Protocol Efficiency: {protocol_efficiency:.2f}%")
    print(f"Total time taken: {total_time_taken:.2f} seconds")
    print(f"Throughput: {throughput:.2f} packets per second")

if __name__ == "__main__":
    random.seed(time.time())
    go_back_n_arq_simulation()
