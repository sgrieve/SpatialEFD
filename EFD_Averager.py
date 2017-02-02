import matplotlib.pyplot as plt
import shapefile as shp
import EFD

coeffList = []

# use a fixed no of harmonics
MaxHarmonic = 17

sf = shp.Reader('/home/sgrieve/Hollow_Processing_Files/Mid_Hollows.shp')


# below here is the real processing of the shapes, above is data i/o

# loop over individual polygons in a multipart shapefile
for shaperec in sf.shapeRecords()[200:500]:

    # Convert the shape instance into a format that EFD can use
    x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

    # Compute the final coefficients using the required number of harmonics and
    # normalize them
    coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
    coeffs = EFD.normalize_efd(coeffs)

    coeffList.append(coeffs)


avg = EFD.AverageCoefficients(coeffList, MaxHarmonic)
sd = EFD.AverageSD(coeffList, avg, MaxHarmonic)

a, b = EFD.inverse_transform(avg, harmonic=MaxHarmonic)
c, d = EFD.inverse_transform(avg + sd, harmonic=MaxHarmonic)
e, f = EFD.inverse_transform(avg - sd, harmonic=MaxHarmonic)


# below here is the plotting of an EFD average, with +/- 1 std dev error bounds

ax = EFD.InitPlot()
EFD.PlotEllipse(ax, a, b, 'k', 2.)
EFD.PlotEllipse(ax, c, d, 'r', 0.5)
EFD.PlotEllipse(ax, e, f, 'b', 0.5)
plt.show()
