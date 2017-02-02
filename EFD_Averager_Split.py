import matplotlib.pyplot as plt
import shapefile as shp
import EFD
import DataLoader

AbovecoeffList = []
BelowcoeffList = []

# use a fixed no of harmonics
MaxHarmonic = 17

sf = shp.Reader('/home/sgrieve/Hollow_Processing_Files/Mid_Hollows.shp')

filename = '/home/sgrieve/Hollow_Processing_Files/Hi_Data_Final_veg_curv.csv'
Below, Above = DataLoader.DataFilter(filename, 'Area', 6000.)

# below here is the real processing of the shapes, above is data i/o

# loop over individual polygons in a multipart shapefile
for shaperec in sf.shapeRecords():
    if shaperec.record in Above:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        AbovecoeffList.append(coeffs)

    elif shaperec.record in Below:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        BelowcoeffList.append(coeffs)


Bavg = EFD.AverageCoefficients(BelowcoeffList, MaxHarmonic)
Bsd = EFD.AverageSD(BelowcoeffList, Bavg, MaxHarmonic)

Aavg = EFD.AverageCoefficients(AbovecoeffList, MaxHarmonic)
Asd = EFD.AverageSD(AbovecoeffList, Aavg, MaxHarmonic)


a, b = EFD.inverse_transform(Aavg, harmonic=MaxHarmonic)
c, d = EFD.inverse_transform(Aavg + Asd, harmonic=MaxHarmonic)
e, f = EFD.inverse_transform(Aavg - Asd, harmonic=MaxHarmonic)

g, h = EFD.inverse_transform(Bavg, harmonic=MaxHarmonic)
i, j = EFD.inverse_transform(Bavg + Bsd, harmonic=MaxHarmonic)
k, l = EFD.inverse_transform(Bavg - Bsd, harmonic=MaxHarmonic)


# below here is the plotting of an EFD average, with +/- 1 std dev error bounds

ax = EFD.InitPlot()
EFD.PlotEllipse(ax, a, b, 'k', 2.)
EFD.PlotEllipse(ax, c, d, 'r', 0.5)
EFD.PlotEllipse(ax, e, f, 'b', 0.5)
EFD.PlotEllipse(ax, g, h, 'k', 2.)
EFD.PlotEllipse(ax, i, j, 'r', 0.5)
EFD.PlotEllipse(ax, k, l, 'b', 0.5)
plt.show()
