import math

class cin_inversa:
    def __init__(self, L1, L2, L3, L4):
        self.L1, self.L2, self.L3, self.L4 = L1, L2, L3, L4
    def calculate_theta(self, (x, y, z, phi)):
        r = math.sqrt(x * x + y * y)
        s = z - self.L1
        Wx = r - self.L4 * math.cos(phi)
        Wz = s - self.L4 * math.sin(phi)

        # Theta1
        theta1 = math.atan(Wz, Wx)
        # Theta3
        theta3 = math.acos((Wx*Wx + Wz*Wz - self.L2*self.L2 - self.L3*self.L3) / (2 * self.L2 * self.L3))
        # Theta2
        theta2 = math.acos(((self.L2 + self.L3 * math.cos(theta3)) * Wx + self.L3 * math.sin(theta3) * Wz) / (Wx*Wx + Wz*Wz))

        #Lower Elbow para Upper Elbow
        theta3 = -theta3
        theta2 = 2 * math.atan(Wz / Wx) - theta2

        #Rodar Theta2 -90º
        theta2 = math.pi / 2 - theta2

        return theta1, theta2, theta3