import tkinter as tk
import ipaddress
import math

class SubNett0r:

    def __init__(self):
        self.root = tk.Tk()
        self.sv1 = None
        self.sv2 = None
        self.sv3 = None
        self.sv4 = None
        self.inverse_subnetmask = None
        self.network_address = None
        self.broadcast = None
        self.ip_range_start = None
        self.ip_range_end = None
        self.setup()

    def setup(self):
        self.sv1 = tk.StringVar()
        self.sv2 = tk.StringVar()
        self.sv3 = tk.StringVar()
        self.sv4 = tk.StringVar()
        self.inverse_subnetmask = tk.StringVar()
        self.network_address = tk.StringVar()
        self.broadcast = tk.StringVar()
        self.ip_range_start = tk.StringVar()
        self.ip_range_end = tk.StringVar()
        # self.sv1.trace("w", lambda ip_address, index, mode, sv1=self.sv1: self.entry_callback_sv1(sv1))
        # self.sv2.trace("w", lambda cidr_suffix, index, mode, sv2=self.sv2: self.entry_callback_sv2(sv2))
        # self.sv3.trace("w", lambda subnet, index, mode, sv3=self.sv3: self.entry_callback_sv3(sv3))
        # self.sv4.trace("w", lambda amount_hosts, index, mode, sv4=self.sv4: self.entry_callback_sv4(sv4))
        self.sv1.set("192.168.132.197")
        # self.sv2.set("24")
        self.sv3.set("255.255.255.0")
        self.sv4.set("254")
        tk.Label(self.root, text="IP-Addresse").grid(row=0)
        tk.Label(self.root, text="CIDR-Suffix").grid(row=1)
        tk.Label(self.root, text="Netzwerkmaske").grid(row=2)
        tk.Label(self.root, text="Inverse Netzwerkmaske: ").grid(row=3)
        tk.Label(self.root, text="Anzahl Hosts").grid(row=4)
        tk.Label(self.root, text="Netzwerkaddresse: ").grid(row=5)
        tk.Label(self.root, text="Broadcast:  ").grid(row=6)
        tk.Label(self.root, text="HOST-IPs von: ").grid(row=7)
        tk.Label(self.root, text="bis: ").grid(row=8)

        e1 = tk.Entry(self.root, textvariable=self.sv1)
        e2 = tk.Entry(self.root, textvariable=self.sv2)
        e3 = tk.Entry(self.root, textvariable=self.sv3)
        e4 = tk.Entry(self.root, textvariable=self.sv4)
        e1.bind('<Return>', (lambda _: self.entry_callback_sv1(e1)))
        e2.bind('<Return>', (lambda _: self.entry_callback_sv2(e2)))
        e3.bind('<Return>', (lambda _: self.entry_callback_sv3(e3)))
        e4.bind('<Return>', (lambda _: self.entry_callback_sv4(e4)))
        inverse_entry = tk.Entry(self.root, textvariable=self.inverse_subnetmask)
        network_entry = tk.Entry(self.root, textvariable=self.network_address)
        broadcast_entry = tk.Entry(self.root, textvariable=self.broadcast)
        ip_range_entry_start = tk.Entry(self.root, textvariable=self.ip_range_start)
        ip_range_entry_end = tk.Entry(self.root, textvariable=self.ip_range_end)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        inverse_entry.grid(row=3, column=1)
        e4.grid(row=4, column=1)
        network_entry.grid(row=5, column=1)
        broadcast_entry.grid(row=6, column=1)
        ip_range_entry_start.grid(row=7, column=1)
        ip_range_entry_end.grid(row=8, column=1)

        inverse_entry.config(state=tk.DISABLED)
        network_entry.config(state=tk.DISABLED)
        broadcast_entry.config(state=tk.DISABLED)
        ip_range_entry_start.config(state=tk.DISABLED)
        ip_range_entry_end.config(state=tk.DISABLED)

        tk.mainloop()

    def entry_callback_sv1(self, sv):
        print("IP Adresse")
        try:
            self.sv2.set(self.get_cidr(self.sv3.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def entry_callback_sv2(self, sv):
        print("CIDR Suffix")
        try:
            cidr = sv.get()
            self.sv3.set(self.get_subnetmask_from_cidr(cidr))
            self.sv4.set(self.get_total_hosts(self.sv3.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def entry_callback_sv3(self, sv):
        print("Netzwerkmaske")
        try:
            mask = sv.get()
            self.sv2.set(self.get_cidr(mask))
            self.sv4.set(self.get_total_hosts(mask))
            self.calculate_other_shit()
        except ValueError:
            pass

    def entry_callback_sv4(self, sv):
        print("Host Callback :)")
        try:
            # RECALCULATE THE FUCKING BROADCAST ADDR
            cidr = self.get_required_subnet_mask_length(sv.get())
            self.sv2.set(cidr)
            self.sv3.set(self.get_subnetmask_from_cidr(cidr))
            self.sv4.set(self.get_total_hosts(self.sv3.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def calculate_other_shit(self):
        self.network_address.set(self.bin_to_ip(self.get_network_addr(self.sv1.get(), self.sv3.get())))
        self.inverse_subnetmask.set(self.bin_to_ip(self.get_invert_mask(self.sv3.get())))
        self.broadcast.set(self.bin_to_ip(self.get_broadcast_addr(self.network_address.get(),
                                                                  self.inverse_subnetmask.get())))
        self.ip_range_start.set(self.get_start_ip(self.network_address.get()))
        self.ip_range_end.set(self.get_end_ip(self.broadcast.get()))

    # Calculations
    def get_cidr(self, mask):
        if mask == '': return "N.A."
        return sum([bin(int(x)).count("1") for x in mask.split(".")])

    def get_total_hosts(self, mask):
        return 2**(32 - self.get_cidr(mask)) - 2

    def get_required_subnet_mask_length(self, amount):
        # Add 2 since 2 IPS are reserved !! IMPORTANT
        length = math.ceil(math.log2(int(amount) + 2))
        return 32 - length

    def get_subnetmask_from_cidr(self, cidr):
        str = '1' * int(cidr)
        return self.bin_to_ip(str.ljust(32, '0'))

    def get_network_addr(self, ip, mask):
        # Convert to Blocks of 8 Bits
        mask = [bin(int(x)+256)[3:] for x in mask.split(".")]
        ip = [bin(int(x)+256)[3:] for x in ip.split(".")]
        result = []
        for a, b in zip(mask, ip):
            mask_8bit = int(a, 2)
            ip_8bit = int(b, 2)
            res = bin(mask_8bit & ip_8bit)[2:].zfill(8)
            result.append(res)
        return result

    def get_broadcast_addr(self, network_addr, invert_mask):
        # Convert to Blocks of 8 Bits
        network_addr = [bin(int(x)+256)[3:] for x in network_addr.split(".")]
        invert_mask = [bin(int(x)+256)[3:] for x in invert_mask.split(".")]
        result = []
        for a, b in zip(network_addr, invert_mask):
            network_addr_8bit = int(a, 2)
            invert_mask_8bit = int(b, 2)
            res = bin(network_addr_8bit | invert_mask_8bit)[2:].zfill(8)
            result.append(res)
        return result

    def get_start_ip(self, ip):
        parts = ip.split('.')
        ip = (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
        ip += 1
        return self.dec_to_ip(ip)

    def get_end_ip(self, ip):
        parts = ip.split('.')
        ip = (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
        ip -= 1
        return self.dec_to_ip(ip)

    def dec_to_ip(self, dec):
        return str(ipaddress.ip_address(dec))

    def bin_to_ip(self, binary):
        binary = "".join(binary)
        return str(ipaddress.ip_address(int(binary, 2)))

    def lazy_bin_to_ip(self, binary):
        return str(ipaddress.IPv4Address("%d.%d.%d.%d" % (binary[0], binary[1], binary[2], binary[3])))

    def get_invert_mask(self, mask):
        mask = [bin(int(x)+256)[3:] for x in mask.split(".")]
        tmp = ''.join(mask)
        result = bin((int(tmp, 2) ^ (2 ** (len(tmp) + 1) - 1)))[3:]
        return result


if __name__ == '__main__':
    SubNett0r()
