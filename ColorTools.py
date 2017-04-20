from __future__ import division

import numpy as np

# from IPython import embed as dbstop

import constants as cc

def lab2xyz(labcolor = ()):

	var_Y = ( labcolor[0] + 16 ) / 116
	var_X = labcolor[1] / 500 + var_Y
	var_Z = var_Y - labcolor[2] / 200

	if (var_Y**3) > 0.008856: 
		var_Y = var_Y**3
	else: 
		var_Y = ( var_Y - 16 / 116 ) / 7.787

	if (var_X**3) > 0.008856: 
		var_X = var_X**3
	else: 
		var_X = ( var_X - 16 / 116 ) / 7.787

	if (var_Z**3) > 0.008856:
		var_Z = var_Z**3
	else: 
		var_Z = ( var_Z - 16 / 116 ) / 7.787

	X = cc.xyz_whitepoint_norm[0] * var_X    
	Y = cc.xyz_whitepoint_norm[1] * var_Y    
	Z = cc.xyz_whitepoint_norm[2] * var_Z    

	return [X,Y,Z]

def xyz2rgb(xyzcolor = ()):
	
	# Convert to rgb using Bradford chromatic adaption for D65
	# return (np.matrix(xyzcolor) * cc.MA)  * cc.M
	
	# xyzcolor = np.matrix([xyzcolor]) * cc.MA

	x = xyzcolor[0] / 100
	y = xyzcolor[1] / 100
	z = xyzcolor[2] / 100

	R = x *  3.2406 + y * -1.5372 + z * -0.4986
	G = x * -0.9689 + y *  1.8758 + z *  0.0415
	B = x *  0.0557 + y * -0.2040 + z *  1.0570

	if  R > 0.0031308:
		R = 1.055 * ( R **( 1 / cc.gamma ) ) - 0.055
	else:
	    R = 12.92 * R

	if G > 0.0031308: 
		G = 1.055 * ( G ** ( 1 / cc.gamma ) ) - 0.055
	else: 
		G = 12.92 * G
	if B > 0.0031308:
		B = 1.055 * ( B ** ( 1 / cc.gamma ) ) - 0.055
	else: 
		B = 12.92 * B	

	R = min(max(R * 255, 0), 255)
	G = min(max(G * 255, 0), 255)
	B = min(max(B * 255, 0), 255)

	return [R,G,B]


def lab2rgb(labcolor = ()):
	rgb = np.array(xyz2rgb(lab2xyz(np.array(labcolor))))

	# if rgb[0] < 0:
	# 	rgb[0] = 0

	# if rgb[0][1] < 0:
	# 	rgb[0][1] = 0

	# if rgb[0][2] < 0:
	# 	rgb[0][2] = 0		
	
	return rgb	

def rgb2psycho(color = ()):

	# color = np.array(color)

	newcolor = np.zeros([3])

	newcolor[0] = 2*(color[0] / 255) - 1
	newcolor[1] = 2*(color[1] / 255) - 1
	newcolor[2] = 2*(color[2] / 255) - 1

	return newcolor

def lab2psycho(color = ()):
	return rgb2psycho(lab2rgb(color))	




# def lab2xyz(labcolor = ()):

# 	#Y
# 	L = labcolor[0] #labcolor[:,0]
# 	L = (L + 16) * (1/116)

# 	if L > (6/29):
# 		L = L ** 3
# 	else:
# 		L = 3*((6/29)**2)*(L - (4/29))

# 	#dum = L > (6/29)
# 	#L[dum] = L[dum]**3
# 	#L[not dum] = 3*((6/29)**2)*(L[not dum] - (4/29))
# 	Y = cc.xyz_whitepoint_norm[1] * L


# 	#X
# 	L = labcolor[0] #labcolor[:,0]
# 	L = (L + 16) * (1/116)
# 	a = labcolor[1]
# 	a = (1/500)*a
# 	X = L + a

# 	if X > (6/29):
# 		X = X ** 3
# 	else:
# 		X = 3*((6/29)**2)*(X - (4/29))

# 	# dum = X > (6/29)
# 	# X[dum]= X[dum]**3
# 	# X[not dum] = 3*((6/29)**2)*(X[not dum] - (4/29))
# 	X = cc.xyz_whitepoint_norm[0] * X


# 	#Z
# 	L = labcolor[0]
# 	L = (L + 16) * (1/116)
# 	b = labcolor[2]
# 	b = (1/200)*b
# 	Z = L - b

# 	if Z > (6/29):
# 		Z = Z ** 3
# 	else:
# 		Z = 3*((6/29)**2)*(Z  - (4/29))

# 	# dum = Z > (6/29)
# 	# Z[dum] = Z[dum]**3
# 	# Z[not dum]  = 3*((6/29)**2)*(Z[not dum]  - (4/29))
# 	Z = cc.xyz_whitepoint_norm[2] * Z


# 	# XYZ
	# return [X, Y, Z]		