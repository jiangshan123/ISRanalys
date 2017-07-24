
# coding: utf-8

def export_ac_Image(image_1D, imageFilename, log = True):
    delta, twotheta = PixelsToAngles(image_1D[:,0], image_1D[:,1])
    Qx, Qy, Qz = AnglesToQ(lamda, th, zeta, delta, twotheta)
    a, c = QToCA(Qx, Qz)

    if log:
        image_1D[:,2] = np.log(image_1D[:,2])
    fig = plt.figure(figsize=(12,10),dpi=100)
    axes = fig.add_axes([0.,0.1,1,0.85]) # left, bottom, width, height (range 0 to 1)
    plt.scatter(c, a, c=image_1D[:,2],rasterized=True, cmap=cm.nipy_spectral,vmin=0,vmax=12)
    plt.xlabel(r'$c$'+'['+r'$\AA$'+']', fontsize=25)
    plt.ylabel(r'$a$'+'['+r'$\AA$'+']', fontsize=25)
    axes.set_aspect('equal')
    
    divider = make_axes_locatable(axes)
    cax = divider.append_axes("right", size="5%", pad=0.3)
    cbar = plt.colorbar(cax=cax)
    cbar.set_label('Log',fontsize=15)
    cbar.ax.tick_params(labelsize=20)
    
    #axes.set_ylim(19.5,6.8)
    #axes.set_xlim(20.1,8.3)

    for tick in axes.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    fig.savefig(imageFilename)

def export_ac_Image_slice(image_1D, imageFilename, log = True):
    delta, twotheta = PixelsToAngles(image_1D[:,0], image_1D[:,1])
    Qx, Qy, Qz = AnglesToQ(lamda, th, zeta, delta, twotheta)
    a, c = QToCA(Qx, Qz)

    if log:
        image_1D[:,2] = np.log(image_1D[:,2])
    fig = plt.figure(figsize=(14,5.5),dpi=100)

    axes = fig.add_axes([0.1,0.11,0.85,0.85]) # left, bottom, width, height (range 0 to 1)
    plt.scatter(c, a, c=image_1D[:,2],rasterized=True, cmap=cm.nipy_spectral,vmin=0,vmax=12)
    plt.xlabel(r'$c$'+'['+r'$\AA$'+']', fontsize=25)
    plt.ylabel(r'$a$'+'['+r'$\AA$'+']', fontsize=25)
    axes.set_aspect('equal')
    
    divider = make_axes_locatable(axes)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    cbar = plt.colorbar(cax=cax)
    cbar.set_label('Log',fontsize=15)
    cbar.ax.tick_params(labelsize=20)
    axes.set_ylim(3.8,4.4)
    axes.set_xlim(3.8,5.51)
    for tick in axes.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    fig.savefig(imageFilename)