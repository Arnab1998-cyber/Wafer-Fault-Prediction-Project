import logging as lg


class logger:
    def __init__(self):
        pass
    def apply_log(self, file_name, msg):
        self.file=file_name
        self.message=msg
        lg.basicConfig(filename=self.file, filemode='a',level=lg.INFO,
                       format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
                       datefmt='%d/%m/%Y  %I:%M:%S %p')
        lg.info(self.message)
