import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

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

contourMapper = vtk.vtkPolyDataMapper()
contourMapper.SetInputConnection(contour.GetOutputPort())
contourMapper.ScalarVisibilityOff()

contourActor = vtk.vtkActor()
contourActor.SetMapper(contourMapper)
contourActor.GetProperty().SetColor( 0.8, 0.7, 0.7 )

interactor = vtk.vtkRenderWindowInteractor()
render_window = vtk.vtkRenderWindow()
render_window.SetSize(600,600)
interactor.SetRenderWindow(render_window);
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

#Important: create OpenGLRenderer for advanced effects
renderer = vtk.vtkOpenGLRenderer()
render_window.AddRenderer(renderer)

light1 = vtk.vtkLight()
light1.SetFocalPoint(0,0,0)
light1.SetPosition(0,10,0.2)
light1.SetColor(0.95,0.97,1.0)
light1.SetIntensity(0.8)
renderer.AddLight(light1)

light2 = vtk.vtkLight()
light2.SetFocalPoint(0,0,0);
light2.SetPosition(10.0,10.0,10.0);
light2.SetColor(1.0,0.8,0.7);
light2.SetIntensity(0.5);
renderer.AddLight(light2);

renderer.SetBackground(0.8,0.8,0.9);
renderer.SetBackground2(1.0,1.0,1.0);
renderer.GradientBackgroundOn();

renderer.AddActor(outlineActor)
renderer.AddActor(contourActor)

#setting up shadow mapping
render_window.SetMultiSamples(0)

basicPasses = vtk.vtkRenderStepsPass()

# Create and add the DOF render pass
dof_pass = vtk.vtkDepthOfFieldPass()
dof_pass.SetDelegatePass(basicPasses);

#When this is on whatever is in the center of the screen is in focus 
dof_pass.AutomaticFocalDistanceOff();
#Tell the renderer to use our render pass pipeline
renderer.SetPass(dof_pass);

#Set the aperture size of the virtual camera. 
#Higher values make the depth of field effect stronger. 
renderer.GetActiveCamera().SetFocalDisk(0.750)

#This point will be in focus
renderer.GetActiveCamera().SetFocalPoint(0, 0, 5)

interactor.Initialize()
render_window.Render()
interactor.Start()