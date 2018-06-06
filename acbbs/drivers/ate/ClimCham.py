# coding=UTF-8

class ClimCham(object):
    def __init__(self, simulate = False):

        #simulation state
        self.simulate = simulate

        if not simulate:
            pass
        else:
            pass

        self.reference_var = None
        self.version_var = None

    @property
    def info(self):
        return {
            "reference":self.reference,
            "version":self.version,
            "error":self.errors,
            "temp_consigne":self.tempConsigne,
            "temp_real":self.tempReal,
            "humidity_consigne":self.humidityConsigne,
            "humidity_real":self.humidityReal
        }

    @property
    def errors(self):
        if not self.simulate:
            return []

        else:
            return []

    @property
    def reference(self):
        if self.reference_var is None:
            #get reference
            self.reference_var = "xxxx"
        return self.reference_var

    @property
    def version(self):
        if self.version_var is None:
            #get reference
            self.version_var = "xxxx"
        return self.version_var

    def enable(self):
        """


        @return  :
        @author
        """
        pass

    @property
    def tempConsigne(self):
        return None

    @property
    def tempReal(self):
        return None

    @property
    def humidityConsigne(self):
        return None

    @property
    def humidityReal(self):
        return None
