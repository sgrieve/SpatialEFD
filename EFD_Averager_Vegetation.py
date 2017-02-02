import matplotlib.pyplot as plt
import shapefile as shp
import EFD
import DataLoader

A = []
B = []
C = []
D = []


# use a fixed no of harmonics
MaxHarmonic = 17

sf = shp.Reader('/home/sgrieve/Hollow_Processing_Files/Mid_Hollows.shp')

filename = '/home/sgrieve/Hollow_Processing_Files/Hi_Data_Final_veg_curv.csv'
a, b, c, d = DataLoader.VegDataFilter(filename)

# below here is the real processing of the shapes, above is data i/o

# loop over individual polygons in a multipart shapefile
for shaperec in sf.shapeRecords():
    if shaperec.record in a:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        A.append(coeffs)

    elif shaperec.record in b:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        B.append(coeffs)

    elif shaperec.record in c:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        C.append(coeffs)

    elif shaperec.record in d:

        # Convert the shape instance into a format that EFD can use
        x, y, contour, NormCentroid = EFD.ProcessGeometry(shaperec)

        # Compute coefficients using the required number of harmonics and
        # normalize them
        coeffs = EFD.CalculateEFD(x, y, MaxHarmonic)
        coeffs = EFD.normalize_efd(coeffs)

        D.append(coeffs)


titles = ['Cove Hardwood', 'Mixed Deciduous', 'Xeric Oak-Pine',
          'Northern Hardwood']

for i, q in enumerate([A, B, C, D]):
    avg = EFD.AverageCoefficients(q, MaxHarmonic)
    sd = EFD.AverageSD(q, avg, MaxHarmonic)

    a, b = EFD.inverse_transform(avg, harmonic=MaxHarmonic)
    c, d = EFD.inverse_transform(avg + sd, harmonic=MaxHarmonic)
    e, f = EFD.inverse_transform(avg - sd, harmonic=MaxHarmonic)

    ax = plt.subplot(2, 2, i + 1)
    ax.axis('equal')
    ax.plot(a, b, 'k', linewidth=2.)
    ax.plot(c, d, 'k', linewidth=1., alpha=0.5)
    ax.plot(e, f, 'k', linewidth=1., alpha=0.5, label=r'$\pm$ 1 std dev')
    plt.title(titles[i])

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off')
    if (i == 3):
        legend = plt.legend(bbox_to_anchor=(1.1, 0), fontsize=12)
        legend.get_frame().set_linewidth(0.)


def mm_to_inch(mm):
    return mm * 0.0393700787

fig = plt.gcf()

#set the size of the plot to be saved. These are the JGR sizes:
#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(190))

plt.savefig('veg_shape.png')
