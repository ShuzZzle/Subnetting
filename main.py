import tkinter as tk
import math


class SubNett0r:

    def __init__(self):
        self.root = tk.Tk()
        self.sv_ipaddr = None
        self.sv_cidr = None
        self.sv_subnetmask = None
        self.sv_hosts = None
        self.inverse_subnetmask = None
        self.network_address = None
        self.broadcast = None
        self.ip_range_start = None
        self.ip_range_end = None
        self.setup()

    def __del__(self):
        pass

    def setup(self):
        self.sv_ipaddr = tk.StringVar()
        self.sv_cidr = tk.StringVar()
        self.sv_subnetmask = tk.StringVar()
        self.sv_hosts = tk.StringVar()
        self.inverse_subnetmask = tk.StringVar()
        self.network_address = tk.StringVar()
        self.broadcast = tk.StringVar()
        self.ip_range_start = tk.StringVar()
        self.ip_range_end = tk.StringVar()

        # Default Values
        self.sv_ipaddr.set("192.168.132.197")
        self.sv_subnetmask.set("255.255.255.0")
        self.sv_hosts.set("254")

        # TK Labels
        tk.Label(self.root, text="IP-Addresse").grid(row=0)
        tk.Label(self.root, text="CIDR-Suffix").grid(row=1)
        tk.Label(self.root, text="Netzwerkmaske").grid(row=2)
        tk.Label(self.root, text="Inverse Netzwerkmaske: ").grid(row=3)
        tk.Label(self.root, text="Anzahl Hosts").grid(row=4)
        tk.Label(self.root, text="Netzwerkaddresse: ").grid(row=5)
        tk.Label(self.root, text="Broadcast:  ").grid(row=6)
        tk.Label(self.root, text="HOST-IPs von: ").grid(row=7)
        tk.Label(self.root, text="bis: ").grid(row=8)

        e1 = tk.Entry(self.root, textvariable=self.sv_ipaddr)
        e2 = tk.Entry(self.root, textvariable=self.sv_cidr)
        e3 = tk.Entry(self.root, textvariable=self.sv_subnetmask)
        e4 = tk.Entry(self.root, textvariable=self.sv_hosts)
        e1.bind('<Return>', (lambda _: self.callback_ipaddr(e1)))
        e2.bind('<Return>', (lambda _: self.callback_cidr(e2)))
        e3.bind('<Return>', (lambda _: self.callback_networkaddr(e3)))
        e4.bind('<Return>', (lambda _: self.callback_host(e4)))
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

    def callback_ipaddr(self, sv):
        try:
            self.sv_cidr.set(self.get_cidr(self.sv_subnetmask.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def callback_cidr(self, sv):
        try:
            cidr = sv.get()
            self.sv_subnetmask.set(self.get_subnetmask_from_cidr(cidr))
            self.sv_hosts.set(self.get_total_hosts(self.sv_subnetmask.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def callback_networkaddr(self, sv):
        try:
            mask = sv.get()
            self.sv_cidr.set(self.get_cidr(mask))
            self.sv_hosts.set(self.get_total_hosts(mask))
            self.calculate_other_shit()
        except ValueError:
            pass

    def callback_host(self, sv):
        try:
            cidr = self.get_required_subnet_mask_length(sv.get())
            self.sv_cidr.set(cidr)
            self.sv_subnetmask.set(self.get_subnetmask_from_cidr(cidr))
            self.sv_hosts.set(self.get_total_hosts(self.sv_subnetmask.get()))
            self.calculate_other_shit()
        except ValueError:
            pass

    def calculate_other_shit(self):
        self.network_address.set(self.bin_to_ip(self.get_network_addr(self.sv_ipaddr.get(), self.sv_subnetmask.get())))
        self.inverse_subnetmask.set(self.bin_to_ip(self.get_invert_mask(self.sv_subnetmask.get())))
        self.broadcast.set(self.bin_to_ip(self.get_broadcast_addr(self.network_address.get(),
                                                                  self.inverse_subnetmask.get())))
        self.ip_range_start.set(self.get_start_ip(self.network_address.get()))
        self.ip_range_end.set(self.get_end_ip(self.broadcast.get()))

    @staticmethod
    def get_cidr(mask):
        return sum([bin(int(x)).count("1") for x in mask.split(".")])

    def get_total_hosts(self, mask):
        return 2**(32 - self.get_cidr(mask)) - 2

    @staticmethod
    def get_required_subnet_mask_length(amount):
        # Add 2 since 2 IPS are reserved !! IMPORTANT
        length = math.ceil(math.log2(int(amount) + 2))
        return 32 - length

    def get_subnetmask_from_cidr(self, cidr):
        mask = '1' * int(cidr)
        return self.bin_to_ip(mask.ljust(32, '0'))

    @staticmethod
    def get_network_addr(ip, mask):
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

    @staticmethod
    def get_broadcast_addr(network_addr, invert_mask):
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

    @staticmethod
    def dec_to_ip(dec):
        return '.'.join(map(lambda _: str(dec >> _ & 0xFF), [24, 16, 8, 0]))

    def bin_to_ip(self, binary):
        binary = "".join(binary)
        return self.dec_to_ip(int(binary, 2))

    @staticmethod
    def get_invert_mask(mask):
        mask = [bin(int(x)+256)[3:] for x in mask.split(".")]
        tmp = ''.join(mask)
        result = bin((int(tmp, 2) ^ (2 ** (len(tmp) + 1) - 1)))[3:]
        return result


if __name__ == '__main__':
    SubNett0r()
