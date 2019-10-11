# Notes:
# *slider issue
# *DoF

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

class sliderCallback(object):
	def __init__(self, actor):
		self.actor = actor
		
	def slide(self, obj, event):
		sliderRep = obj.GetRepresentation()
		val = sliderRep.GetValue()
		contour2.SetDistance(val)
		
class sliderCallback2(object):
	def __init__(self, actor):
		self.actor = actor
		
	def slide2(self, obj, event):
		sliderRep2 = obj.GetRepresentation()
		val2 = sliderRep2.GetValue()
		contour2.SetIncrement(math.Round(val2))
		
class sliderCallback3(object):
	def __init__(self, actor):
		self.actor = actor
		
	def slide3(self, obj, event):
		sliderRep3 = obj.GetRepresentation()
		val3 = sliderRep3.GetValue()
		contour.SetValue(0, math.Round(val3))
		contour2.SetValue(math.Round(val3))
		
class sliderCallback4(object):
	def __init__(self, actor):
		self.actor = actor
		
	def slide4(self, obj, event):
		valR = sliderRep4.GetValue()
		valG = sliderRep5.GetValue()
		valB = sliderRep6.GetValue()
		contourActor.GetProperty().SetColor( valR, valG, valB )

math=vtk.vtkMath
		
reader = vtk.vtkMetaImageReader()
reader.SetFileName("aneurism.mhd")
reader.Update()

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

contour = vtk.vtkMarchingCubes() 
contour.SetInputConnection(reader.GetOutputPort()) 
contour.SetValue(0, 128)
contour.Update()

contour2 = vtk.vtkRecursiveDividingCubes() 
contour2.SetInputConnection(reader.GetOutputPort()) 
contour2.SetValue(128)
contour2.SetDistance(2)
contour2.SetIncrement(1)
contour2.Update()

planes = vtk.vtkPlanes()

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(contour.GetOutputPort())
clipper.SetClipFunction(planes)
clipper.InsideOutOn()

contourMapper = vtk.vtkPolyDataMapper()
contourMapper.SetInputConnection(clipper.GetOutputPort())
contourMapper.ScalarVisibilityOff()

contourActor = vtk.vtkActor()
contourActor.SetMapper(contourMapper)
contourActor.GetProperty().SetColor( 0.8, 0.7, 0.7 )

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

ren.AddActor(outlineActor)
ren.AddActor(contourActor)
renWin.SetSize(600, 600)
ren.SetBackground(0.3, 0.3, 0.4)

iact = vtk.vtkRenderWindowInteractor()
iact.SetRenderWindow(renWin)
iact.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

boxWidget = vtk.vtkBoxWidget()
boxWidget.SetInteractor(iact)
boxWidget.SetPlaceFactor(1.25)

#BUTTON1 START-------------------------------------!
def textImage(text):
	buttonImage = vtk.vtkImageData()
	freeType = vtk.vtkFreeTypeStringToImage()
	textProperty = vtk.vtkTextProperty()
	textProperty.SetColor(1.0, 1.0, 1.0)
	textProperty.SetFontSize(64);
	textProperty.SetFontFamilyToTimes()
	freeType.RenderString(textProperty, text, 120, buttonImage, [0,0]);
	return buttonImage

wireframe= False

def togwire(obj, event):
	global wireframe
	wireframe = not wireframe
	if (wireframe == True):
		contourActor.GetProperty().SetRepresentationToWireframe()
	else:
		contourActor.GetProperty().SetRepresentationToSurface()
	
wire_image = textImage("Wireframe Off")
wire_image2 = textImage("Wireframe On")
buttonRep = vtk.vtkTexturedButtonRepresentation2D()
buttonRep.SetNumberOfStates(2);
buttonRep.SetButtonTexture(0, wire_image);
buttonRep.SetButtonTexture(1, wire_image2);
buttonRep.PlaceWidget([0, 250, 0, 50, 0, 50]);

buttonWidget = vtk.vtkButtonWidget()
buttonWidget.SetInteractor(iact)
buttonWidget.SetRepresentation(buttonRep)
buttonWidget.SetEnabled(True)
buttonWidget.On()
buttonWidget.AddObserver("StateChangedEvent", togwire)
#BUTTON1 END----------------------------------!

#BUTTON2 START-------------------------------------!
def textImage2(text):
	buttonImage2 = vtk.vtkImageData()
	freeType2 = vtk.vtkFreeTypeStringToImage()
	textProperty2 = vtk.vtkTextProperty()
	textProperty2.SetColor(1.0, 1.0, 1.0)
	textProperty2.SetFontSize(64);
	textProperty2.SetFontFamilyToTimes()
	freeType2.RenderString(textProperty2, text, 120, buttonImage2, [0,0]);
	return buttonImage2

inter= False

def toginter(obj, event):
	global inter
	inter = not inter
	if (inter == True):
		clipper.SetInputConnection(contour2.GetOutputPort())
	else:
		clipper.SetInputConnection(contour.GetOutputPort())
		
inter_image = textImage2("Marching Cubes")
inter_image2 = textImage2("Dividing Cubes")
buttonRep2 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep2.SetNumberOfStates(2);
buttonRep2.SetButtonTexture(0, inter_image);
buttonRep2.SetButtonTexture(1, inter_image2);
buttonRep2.PlaceWidget([250, 500, 0, 50, 0, 50]);

buttonWidget2 = vtk.vtkButtonWidget()
buttonWidget2.SetInteractor(iact)
buttonWidget2.SetRepresentation(buttonRep2)
buttonWidget2.SetEnabled(True)
buttonWidget2.On()
buttonWidget2.AddObserver("StateChangedEvent", toginter)
#BUTTON2 END----------------------------------!

#BUTTON3 START-------------------------------------!
def textImage3(text):
	buttonImage3 = vtk.vtkImageData()
	freeType3 = vtk.vtkFreeTypeStringToImage()
	textProperty3 = vtk.vtkTextProperty()
	textProperty3.SetColor(1.0, 1.0, 1.0)
	textProperty3.SetFontSize(64);
	textProperty3.SetFontFamilyToTimes()
	freeType3.RenderString(textProperty3, text, 120, buttonImage3, [0,0]);
	return buttonImage3

clip= False

def togdata(obj, event):
	global clip
	clip = not clip
	if (clip == True):
		boxWidget.Off()
	else:
		boxWidget.On()
	
swap_image = textImage3("Hide Clipping Box")
swap_image2 = textImage3("Show Clipping Box")
buttonRep3 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep3.SetNumberOfStates(2);
buttonRep3.SetButtonTexture(0, swap_image);
buttonRep3.SetButtonTexture(1, swap_image2);
buttonRep3.PlaceWidget([500, 750, 0, 50, 0, 50]);

buttonWidget3 = vtk.vtkButtonWidget()
buttonWidget3.SetInteractor(iact)
buttonWidget3.SetRepresentation(buttonRep3)
buttonWidget3.SetEnabled(True)
buttonWidget3.On()
buttonWidget3.AddObserver("StateChangedEvent", togdata)
#BUTTON3 END----------------------------------!

#BUTTON4 START-------------------------------------!
def textImage4(text):
	buttonImage4 = vtk.vtkImageData()
	freeType4 = vtk.vtkFreeTypeStringToImage()
	textProperty4 = vtk.vtkTextProperty()
	textProperty4.SetColor(1.0, 1.0, 1.0)
	textProperty4.SetFontSize(64);
	textProperty4.SetFontFamilyToTimes()
	freeType4.RenderString(textProperty4, text, 120, buttonImage4, [0,0]);
	return buttonImage4

slide= False

def togslide(obj, event):
	global slide
	slide = not slide
	if (slide == True):
		sliderWidget.SetEnabled(False)
		sliderWidget2.SetEnabled(False)
		sliderWidget3.SetEnabled(False)
		sliderWidget4.SetEnabled(False)
		sliderWidget5.SetEnabled(False)
		sliderWidget6.SetEnabled(False)
	else:
		sliderWidget.SetEnabled(True)
		sliderWidget2.SetEnabled(True)
		sliderWidget3.SetEnabled(True)
		sliderWidget4.SetEnabled(True)
		sliderWidget5.SetEnabled(True)
		sliderWidget6.SetEnabled(True)
	
swap_image = textImage4("Hide Sliders")
swap_image2 = textImage4("Show Sliders")
buttonRep4 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep4.SetNumberOfStates(2);
buttonRep4.SetButtonTexture(0, swap_image);
buttonRep4.SetButtonTexture(1, swap_image2);
buttonRep4.PlaceWidget([750, 1000, 0, 50, 0, 50]);

buttonWidget4 = vtk.vtkButtonWidget()
buttonWidget4.SetInteractor(iact)
buttonWidget4.SetRepresentation(buttonRep4)
buttonWidget4.SetEnabled(True)
buttonWidget4.On()
buttonWidget4.AddObserver("StateChangedEvent", togslide)
#BUTTON4 END----------------------------------!

#BUTTON5 START-------------------------------------!
def textImage5(text):
	buttonImage5 = vtk.vtkImageData()
	freeType5 = vtk.vtkFreeTypeStringToImage()
	textProperty5 = vtk.vtkTextProperty()
	textProperty5.SetColor(1.0, 1.0, 1.0)
	textProperty5.SetFontSize(64);
	textProperty5.SetFontFamilyToTimes()
	freeType5.RenderString(textProperty5, text, 120, buttonImage5, [0,0]);
	return buttonImage5

mpr= False

def togmpr(obj, event):
	global mpr
	mpr = not mpr
	if (mpr == True):
		planeWidgetX.On()
		planeWidgetY.On()
		planeWidgetZ.On()
		ren.RemoveActor(contourActor)
	else:
		planeWidgetX.Off()
		planeWidgetY.Off()
		planeWidgetZ.Off()
		ren.AddActor(contourActor)
	
swap_image = textImage5("Show MPR")
swap_image2 = textImage5("Hide MPR")
buttonRep5 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep5.SetNumberOfStates(2);
buttonRep5.SetButtonTexture(0, swap_image);
buttonRep5.SetButtonTexture(1, swap_image2);
buttonRep5.PlaceWidget([1000, 1250, 0, 50, 0, 50]);

buttonWidget5 = vtk.vtkButtonWidget()
buttonWidget5.SetInteractor(iact)
buttonWidget5.SetRepresentation(buttonRep5)
buttonWidget5.SetEnabled(True)
buttonWidget5.On()
buttonWidget5.AddObserver("StateChangedEvent", togmpr)
#BUTTON5 END----------------------------------!

# This callback function does the actual work: updates the vtkPlanes
# implicit function.  This in turn causes the pipeline to update.
def ClipPolygons(object, event):
	global contourActor, planes
	object.GetPlanes(planes)

#boxwidget
reader.Update()
boxWidget.SetInputConnection(reader.GetOutputPort())
boxWidget.PlaceWidget()
boxWidget.AddObserver("InteractionEvent", ClipPolygons)
boxWidget.On()
boxWidget.RotationEnabledOff()
boxWidget.GetPlanes(planes)

#distance slider
sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.SetValue(2);
sliderRep.SetMinimumValue(1);
sliderRep.SetMaximumValue(2);
sliderRep.SetTitleText("Distance");
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep.GetPoint1Coordinate().SetValue(0.1,0.9)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep.GetPoint2Coordinate().SetValue(0.9,0.9)
sliderRep.SetSliderLength(0.02);
sliderRep.SetSliderWidth(0.03);
sliderRep.SetEndCapLength(0.01);
sliderRep.SetEndCapWidth(0.03);
sliderRep.SetTubeWidth(0.005);

sliderWidget = vtk.vtkSliderWidget()
sliderWidget.SetInteractor(iact)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.SetAnimationModeToAnimate()
sliderWidget.SetEnabled(True)

sc = sliderCallback(contourActor)
sliderWidget.AddObserver("EndInteractionEvent", sc.slide)

#increment slider
sliderRep2 = vtk.vtkSliderRepresentation2D()
sliderRep2.SetValue(1);
sliderRep2.SetMinimumValue(0);
sliderRep2.SetMaximumValue(10);
sliderRep2.SetTitleText("Increment");
sliderRep2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep2.GetPoint1Coordinate().SetValue(0.1,0.8);
sliderRep2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep2.GetPoint2Coordinate().SetValue(0.9,0.8)
sliderRep2.SetSliderLength(0.02);
sliderRep2.SetSliderWidth(0.03);
sliderRep2.SetEndCapLength(0.01);
sliderRep2.SetEndCapWidth(0.03);
sliderRep2.SetTubeWidth(0.005);

sliderWidget2 = vtk.vtkSliderWidget()
sliderWidget2.SetInteractor(iact)
sliderWidget2.SetRepresentation(sliderRep2)
sliderWidget2.SetAnimationModeToAnimate();
sliderWidget2.SetEnabled(True)

sc2 = sliderCallback2(contourActor)
sliderWidget2.AddObserver("EndInteractionEvent", sc2.slide2)


#isocontour slider
sliderRep3 = vtk.vtkSliderRepresentation2D()
sliderRep3.SetValue(128);
sliderRep3.SetMinimumValue(0);
sliderRep3.SetMaximumValue(255);
sliderRep3.SetTitleText("Isovalue");
sliderRep3.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep3.GetPoint1Coordinate().SetValue(0.1,0.7);
sliderRep3.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep3.GetPoint2Coordinate().SetValue(0.9,0.7)
sliderRep3.SetSliderLength(0.02);
sliderRep3.SetSliderWidth(0.03);
sliderRep3.SetEndCapLength(0.01);
sliderRep3.SetEndCapWidth(0.03);
sliderRep3.SetTubeWidth(0.005);

sliderWidget3 = vtk.vtkSliderWidget()
sliderWidget3.SetInteractor(iact)
sliderWidget3.SetRepresentation(sliderRep3)
sliderWidget3.SetAnimationModeToAnimate();
sliderWidget3.SetEnabled(True)

sc3 = sliderCallback3(contourActor)
sliderWidget3.AddObserver("EndInteractionEvent", sc3.slide3)

#R slider
sliderRep4 = vtk.vtkSliderRepresentation2D()
sliderRep4.SetValue(0.8);
sliderRep4.SetMinimumValue(0);
sliderRep4.SetMaximumValue(1);
sliderRep4.SetTitleText("R");
sliderRep4.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep4.GetPoint1Coordinate().SetValue(0.1,0.6);
sliderRep4.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep4.GetPoint2Coordinate().SetValue(0.3,0.6)
sliderRep4.SetSliderLength(0.02);
sliderRep4.SetSliderWidth(0.03);
sliderRep4.SetEndCapLength(0.01);
sliderRep4.SetEndCapWidth(0.03);
sliderRep4.SetTubeWidth(0.005);

sliderWidget4 = vtk.vtkSliderWidget()
sliderWidget4.SetInteractor(iact)
sliderWidget4.SetRepresentation(sliderRep4)
sliderWidget4.SetAnimationModeToAnimate();
sliderWidget4.SetEnabled(True)

sc4 = sliderCallback4(contourActor)
sliderWidget4.AddObserver("InteractionEvent", sc4.slide4)

#G slider
sliderRep5 = vtk.vtkSliderRepresentation2D()
sliderRep5.SetValue(0.7);
sliderRep5.SetMinimumValue(0);
sliderRep5.SetMaximumValue(1);
sliderRep5.SetTitleText("G");
sliderRep5.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep5.GetPoint1Coordinate().SetValue(0.4,0.6);
sliderRep5.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep5.GetPoint2Coordinate().SetValue(0.6,0.6)
sliderRep5.SetSliderLength(0.02);
sliderRep5.SetSliderWidth(0.03);
sliderRep5.SetEndCapLength(0.01);
sliderRep5.SetEndCapWidth(0.03);
sliderRep5.SetTubeWidth(0.005);

sliderWidget5 = vtk.vtkSliderWidget()
sliderWidget5.SetInteractor(iact)
sliderWidget5.SetRepresentation(sliderRep5)
sliderWidget5.SetAnimationModeToAnimate();
sliderWidget5.SetEnabled(True)

sliderWidget5.AddObserver("InteractionEvent", sc4.slide4)

#B slider
sliderRep6 = vtk.vtkSliderRepresentation2D()
sliderRep6.SetValue(0.7);
sliderRep6.SetMinimumValue(0);
sliderRep6.SetMaximumValue(1);
sliderRep6.SetTitleText("B");
sliderRep6.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep6.GetPoint1Coordinate().SetValue(0.7,0.6);
sliderRep6.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay();
sliderRep6.GetPoint2Coordinate().SetValue(0.9,0.6)
sliderRep6.SetSliderLength(0.02);
sliderRep6.SetSliderWidth(0.03);
sliderRep6.SetEndCapLength(0.01);
sliderRep6.SetEndCapWidth(0.03);
sliderRep6.SetTubeWidth(0.005);

sliderWidget6 = vtk.vtkSliderWidget()
sliderWidget6.SetInteractor(iact)
sliderWidget6.SetRepresentation(sliderRep6)
sliderWidget6.SetAnimationModeToAnimate();
sliderWidget6.SetEnabled(True)

sliderWidget6.AddObserver("InteractionEvent", sc4.slide4)

#annotation widget
axesActor = vtk.vtkAnnotatedCubeActor();
axesActor.SetXPlusFaceText('X+')
axesActor.SetXMinusFaceText('X-')
axesActor.SetYMinusFaceText('Y-')
axesActor.SetYPlusFaceText('Y+')
axesActor.SetZMinusFaceText('Z-')
axesActor.SetZPlusFaceText('Z+')
axesActor.GetTextEdgesProperty().SetColor(0,0,0)
axesActor.GetTextEdgesProperty().SetLineWidth(2)
axesActor.GetCubeProperty().SetColor(0.5,0.5,0.5)
axes = vtk.vtkOrientationMarkerWidget()
axes.SetOrientationMarker(axesActor)
axes.SetInteractor(iact)
axes.EnabledOn()
axes.InteractiveOn()
ren.ResetCamera()

# multiplanar reformatting
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

planeWidgetX = vtk.vtkImagePlaneWidget()
planeWidgetX.SetResliceInterpolateToLinear()
planeWidgetX.DisplayTextOn()
planeWidgetX.SetInputConnection(reader.GetOutputPort())
planeWidgetX.SetPlaneOrientationToXAxes()
planeWidgetX.SetSliceIndex(128)
planeWidgetX.SetPicker(picker)
planeWidgetX.SetKeyPressActivationValue("x")

prop1 = planeWidgetX.GetPlaneProperty()
prop1.SetColor(1, 0, 0)


planeWidgetY = vtk.vtkImagePlaneWidget()
planeWidgetY.SetResliceInterpolateToLinear()
planeWidgetY.DisplayTextOn()
planeWidgetY.SetInputConnection(reader.GetOutputPort())
planeWidgetY.SetPlaneOrientationToYAxes()
planeWidgetY.SetSliceIndex(128)
planeWidgetY.SetPicker(picker)
planeWidgetY.SetKeyPressActivationValue("y")

prop2 = planeWidgetY.GetPlaneProperty()
prop2.SetColor(1,1,0)

planeWidgetZ = vtk.vtkImagePlaneWidget()
planeWidgetZ.SetResliceInterpolateToLinear()
planeWidgetZ.DisplayTextOn()
planeWidgetZ.SetInputConnection(reader.GetOutputPort())
planeWidgetZ.SetPlaneOrientationToZAxes()
planeWidgetZ.SetSliceIndex(128)
planeWidgetZ.SetPicker(picker)
planeWidgetZ.SetKeyPressActivationValue("z")

prop3 = planeWidgetZ.GetPlaneProperty()
prop3.SetColor(0,0,1)

planeWidgetX.SetInteractor(iact)
planeWidgetX.Off()
planeWidgetY.SetInteractor(iact)
planeWidgetY.Off()
planeWidgetZ.SetInteractor(iact)
planeWidgetZ.Off()

#shadow & DOF
light1 = vtk.vtkLight()
light1.SetFocalPoint(0,0,0)
light1.SetPosition(0,10,0.2)
light1.SetColor(0.95,0.97,1.0)
light1.SetIntensity(0.8)
ren.AddLight(light1)

light2 = vtk.vtkLight()
light2.SetFocalPoint(0,0,0);
light2.SetPosition(10.0,10.0,10.0);
light2.SetColor(1.0,0.8,0.7);
light2.SetIntensity(0.5);
ren.AddLight(light2);

renWin.SetMultiSamples(0)

basicPasses = vtk.vtkRenderStepsPass()

# dof_pass = vtk.vtkDepthOfFieldPass()
# dof_pass.SetDelegatePass(basicPasses);
# dof_pass.AutomaticFocalDistanceOff();
# ren.SetPass(dof_pass);
# ren.GetActiveCamera().SetFocalDisk(0.250)
# ren.GetActiveCamera().SetFocalPoint(0, 0, 0)

iact.Initialize()
renWin.Render()
iact.Start()

