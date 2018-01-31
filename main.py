import tkinter as tk


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
        self.sv1.trace("w", lambda ip_address, index, mode, sv1=self.sv1: self.entry_callback(sv1))
        self.sv2.trace("w", lambda cidr_suffix, index, mode, sv2=self.sv2: self.entry_callback(sv2))
        self.sv3.trace("w", lambda subnet, index, mode, sv3=self.sv3: self.entry_callback(sv3))
        self.sv4.trace("w", lambda amount_hosts, index, mode, sv4=self.sv4: self.entry_callback(sv4))
        self.sv1.set("192.168.132.197")
        # self.sv2.set("24")
        self.sv3.set("255.255.255.0")
        self.sv4.set("254")
        self.inverse_subnetmask.set("Inverse Netzwerkmaske: ")
        self.network_address.set("Netzwerk Addresse: ")
        self.broadcast.set("Broadcast: ")
        self.ip_range_start.set("HOST-IPs von: ")
        self.ip_range_end.set("Bis: ")
        tk.Label(self.root, text="IP-Addresse").grid(row=0)
        tk.Label(self.root, text="CIDR-Suffix").grid(row=1)
        tk.Label(self.root, text="Netzwerkmaske").grid(row=2)
        tk.Label(self.root, text="Inverse Netzwerkmaske: ", textvariable=self.inverse_subnetmask).grid(row=3)
        tk.Label(self.root, text="Anzahl Hosts").grid(row=4)
        tk.Label(self.root, text="Netzwerkaddresse: ",  textvariable=self.network_address).grid(row=5)
        tk.Label(self.root, text="Broadcast:  ", textvariable=self.broadcast).grid(row=6)
        tk.Label(self.root, text="HOST-IPs von: ",  textvariable=self.ip_range_start).grid(row=7)
        tk.Label(self.root, text="bis: ",  textvariable=self.ip_range_end).grid(row=8)

        e1 = tk.Entry(self.root, textvariable=self.sv1)
        e2 = tk.Entry(self.root, textvariable=self.sv2)
        e3 = tk.Entry(self.root, textvariable=self.sv3)
        e4 = tk.Entry(self.root, textvariable=self.sv4)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        e4.grid(row=4, column=1)

        tk.mainloop()

    def entry_callback(self, sv):
        # print(sv.get())
        self.sv2.set(self.get_cidr(self.sv3.get()))


    # Calculations
    def get_cidr(self, mask):
        if mask == '': return "N.A."
        return sum([bin(int(x)).count("1") for x in mask.split(".")])


if __name__ == '__main__':
    SubNett0r()
