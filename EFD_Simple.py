import matplotlib.pyplot as plt
import shapefile as shp
import EFD


sf = shp.Reader('/home/sgrieve/Hollow_Processing_Files/Mid_Hollows.shp')
shaperec = sf.shapeRecords()[236]

# below here is the real processing of the shapes, above is data i/o

# Convert the shape instance into a format that EFD can use
x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

# get the maximum number of harmonics
# this is done by using the nyquist frequency, then using those coeffs
# to get the MaxHarmonic needed to represent 0.9999 of the spectral power
nHarmonics = EFD.Nyquist(contour)
coeffs = EFD.CalculateEFD(x, y, nHarmonics)
MaxHarmonic = EFD.FourierPower(coeffs, contour)

# Compute the final coefficients using the required number of harmonics and
# normalize them
coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
coeffs = EFD.normalize_efd(coeffs)

# get the locus of the coefficients and use it to perform the inverse_transform
locus = EFD.calculate_dc_coefficients(contour)
xt, yt = EFD.inverse_transform(coeffs, locus=locus, harmonic=MaxHarmonic)


# below here is the plotting of an EFD shape

ax = EFD.InitPlot()
EFD.PlotEllipse(ax, xt, yt, 'k', 2.)
plt.show()
