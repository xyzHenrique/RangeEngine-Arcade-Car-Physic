def lerp(a, b, t):
  """
  Linearly interpolates between two values.

  Args:
    a: The first value.
    b: The second value.
    t: The interpolation factor.

  Returns:
    The interpolated value.
  """

  return (1 - t) * a + t * b

def clamp(value, a_min, a_max):
  """
  Clamps a value to a specified range.

  Args:
    value: The value to be clamped.
    a_min: The minimum value of the range.
    a_max: The maximum value of the range.

  Returns:
    The clamped value.
  """

  if value < a_min:
    value = a_min
  elif value > a_max:
    value = a_max
  return value

def smooth(start, end, factor):
    """
    Performs smoothing on a specified range.
    
    Args:
        i: The initial value.
        f: The final value.
        s: The smoothing factor.
    
    Returns:
        The smoothed value.
    """
    
    factor = max(factor, 1.0)  # Garante que o fator seja pelo menos 1.0
    smoothed_values = [start + (end - start) * i / (factor - 1) for i in range(int(factor))]
    smoothed_values.append(end)  # Adiciona o valor final
    return smoothed_values

def timer(i, f):
    """
    Performs timing using a BGE RealTime Logic.
    
    Args:
        i: The initial value.
        f: The final value.
    
    Returns:
        The timing value.
    """

    return logic.getRealTime() - i >= f
       
def get_driver_ratio(input, output):
  """
  Calculates the driver ratio based on input and output values.
      
  Parameters:
    - input: Input value (e.g., number of teeth on the input gear).
    - output: Output value (e.g., number of teeth on the output gear).
    
  Returns:
    - The calculated driver ratio (input / output).
  """
  return input / output

def get_tire_circumference(tire_width_mm, aspect_ratio, wheel_diameter_inches):
  """
  Calculates the tire circumference based on tire width, aspect ratio, and wheel diameter.
    
  Parameters:
    - tire_width_mm: Width of the tire in millimeters.
    - aspect_ratio: Aspect ratio of the tire (percentage).
    - wheel_diameter_inches: Diameter of the wheel in inches.
    
  Returns:
    - The calculated tire circumference in meters.
  """
  # Convert tire width from millimeters to meters
  tire_width_meters = tire_width_mm / 1000

  # Calculate tire height in meters using aspect ratio
  tire_height_meters = tire_width_meters * (aspect_ratio / 100)

  # Calculate tire radius in meters (half of wheel diameter)
  tire_radius_meters = (wheel_diameter_inches * 0.0254) / 2

  # Calculate tire circumference in meters
  tire_circumference_meters = 2 * 3.1416 * (tire_radius_meters + tire_height_meters)

  return tire_circumference_meters