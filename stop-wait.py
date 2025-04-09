import random
import time

MAX_RETRANSMISSIONS = 5
LOSS_PROBABILITY = 0.2        
ACK_LOSS_PROBABILITY = 0.2    
ROUND_TRIP_TIME = 1           
TIMEOUT = 2                    
PACKET_SIZE = 1024            

def is_packet_lost():
    return random.random() < LOSS_PROBABILITY

def is_ack_lost():
    return random.random() < ACK_LOSS_PROBABILITY

def send_packet(packet_num):
    retransmissions = 0
    ack_received = False

    while retransmissions < MAX_RETRANSMISSIONS:
        print(f"Sending packet {packet_num}...")

        if is_packet_lost():
            print(f"Packet {packet_num} is lost.")
            retransmissions += 1
            time.sleep(ROUND_TRIP_TIME)
            continue

        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            if is_ack_lost():
                print(f"ACK for packet {packet_num} is lost.")
                break
            else:
                ack_received = True
                break

        if ack_received:
            print(f"ACK for packet {packet_num} received.")
            return retransmissions
        else:
            print(f"ACK for packet {packet_num} not received, resending...")
            retransmissions += 1
            time.sleep(ROUND_TRIP_TIME)

    print(f"Packet {packet_num} failed to send after {MAX_RETRANSMISSIONS} attempts.")
    return retransmissions

def main():
    random.seed(time.time())
    file_packets = ["Packet 1", "Packet 2", "Packet 3", "Packet 4", "Packet 5"]
    total_packets = len(file_packets)
    total_retransmissions = 0
    total_sent_packets = 0

    start_time = time.time()

    for i, packet in enumerate(file_packets):
        print(f"\n----- Sending {packet} -----")
        retransmissions = send_packet(i + 1)
        total_retransmissions += retransmissions
        total_sent_packets += 1

    end_time = time.time()
    total_time = end_time - start_time

    total_data_sent = total_sent_packets * PACKET_SIZE
    throughput = total_data_sent / total_time if total_time > 0 else 0
    efficiency = ((total_sent_packets - total_retransmissions) / total_sent_packets) * 100

    print("\nTransmission Report:")
    print(f"Total packets sent: {total_sent_packets}")
    print(f"Total retransmissions: {total_retransmissions}")
    print(f"Protocol efficiency: {efficiency:.2f}%")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Throughput: {throughput:.2f} bytes per second")

if __name__ == "__main__":
    main()
