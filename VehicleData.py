class VehicleData:

    def __init__(self):
        self.Vehicle_ID = None
        self.Frame_ID = None

        self.Total_Frames = None
        self.Global_Time = None
        self.Local_X = None
        self.Local_Y = None
        self.Global_X = None
        self.Global_Y = None

        self.v_Length_ft = None
        self.v_Width_ft = None

        self.v_Length_metric = None
        self.v_Width_metric = None

        self.v_Class = None

        self.Lane_ID = None
        self.Preceding = []
        self.Following = []
        self.Space_Headway = None
        self.Time_Headway = None

        self.frames = []
        self.v_Vel_ft = []
        self.v_Acc_ft = []

        self.v_Vel_metric = []
        self.v_Acc_metric = []
