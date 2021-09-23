from astropy.io import fits
import numpy as np
import scipy.constants as cst
###############################################################################
class MangaProcess:
    def __init__(self):
        pass

    def get_data(self,
        plate_ifu:'str', data_directory:'str'):
        """
        Get relevant data

        PARAMETERS

            plate_ifu: galaxy identifier [sdss, manga]
            data_directory: directory location of the data cube

        OUTPUT

            tuple with wavelength, raw flux and stellar velocity field arrays
        """

        data_location = (f"{data_directory}/"
            f"manga-{plate_ifu}-LOGCUBE-HYB10-GAU-MILESHC.fits.gz"
            )

        with fits.open(data_location) as cube:

            # Re-order FLUX, IVAR, and MASK arrays
            # (wavelength, DEC, RA) to (RA, DEC, wavelength)

            wave = cube['wave'].data
            raw_flux = np.transpose(cube['FLUX'].data, axes=(2, 1, 0))
            # ivar = np.transpose(cube['IVAR'].data, axes=(2, 1, 0))
            # mask = np.transpose(cube['MASK'].data, axes=(2, 1, 0))
            # get units
            # flux_header = cube['FLUX'].header

        with fits.open(data_location.replace('LOGCUBE', 'MAPS')) as maps:

            stellar_velocity_field = maps['STELLAR_VEL'].data

        return [wave, raw_flux, stellar_velocity_field]

    def save_to_table(self):
        pass

    def correct_for_rotation(self,
        raw_flux:'np.array',
        wave:'np.array',
        wave_master:'np.array',
        velocity_field:'np.array'
        ):
        """
        Correct doppler shift introduced by rotation
        PARAMETERS
        OUTPUT
        """
        number_x, number_y, number_z = raw_flux.shape

        flux = np.empty( (number_x*number_y, wave_master.size) )

        raw_flux = raw_flux.reshape(number_x*number_y, number_z)

        for idx, velocity in enumerate(velocity_field.reshape(-1)):

            flux[idx, :] = np.interp(
                wave_master,
                wave*cst.c/(cst.c + velocity*1_000),
                raw_flux[idx, :],
                left=np.nan,
                right=np.nan
                )

        # Not sure because spaxels are correlated and here the idea is to keep
        # it that way
        #     median = np.nanmedian(flux[idx, :])
        #     if median != 0:
        #         flux[idx, :] *= 1./median
        flux = flux.reshape(number_x, number_y, wave_master.size)


        return flux
    ###############################################################################
