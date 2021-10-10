import logging
import epdconfig

# Display resolution
EPD_WIDTH = 400
EPD_HEIGHT = 300

logger = logging.getLogger(__name__)


class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(5)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        logger.debug("e-Paper busy")
        self.send_command(0x71);
        while (epdconfig.digital_read(self.busy_pin) == 0):  # 0: idle, 1: busy
            self.send_command(0x71);
            epdconfig.delay_ms(20)
        logger.debug("e-Paper busy release")

    def init(self):
        if (epdconfig.module_init() != 0):
            return -1

        self.reset()

        self.send_command(0x04);
        self.ReadBusy();

        self.send_command(0x00);
        self.send_data(0x0f);

        return 0

    def getbuffer(self, image):
        # logger.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logger.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if (imwidth == self.width and imheight == self.height):
            logger.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif (imwidth == self.height and imheight == self.width):
            logger.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, imageblack, imagered):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])

        self.send_command(0x12)
        epdconfig.delay_ms(20)
        self.ReadBusy()

    def Clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        self.send_command(0x12)
        epdconfig.delay_ms(20)
        self.ReadBusy()

    def sleep(self):
        self.send_command(0X50);
        self.send_data(0xf7);  # border floating

        self.send_command(0X02);  # power off
        self.ReadBusy();  # waiting for the electronic paper IC to release the idle signal
        self.send_command(0X07);  # deep sleep
        self.send_data(0xA5);

        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
### END OF FILE ###
