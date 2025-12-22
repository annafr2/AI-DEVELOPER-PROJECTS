import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Step 3: 360-degree rotation with animation

def create_rectangle():
    """Create a rectangle with 4 vertices"""
    width = 4
    height = 2
    vertices = np.array([
        [-width/2, -height/2],  # bottom-left vertex
        [width/2, -height/2],   # bottom-right vertex  
        [width/2, height/2],    # top-right vertex
        [-width/2, height/2]    # top-left vertex
    ])
    return vertices

def create_rotation_matrix(angle_degrees):
    """Create rotation matrix for given angle"""
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    return rotation_matrix

def rotate_rectangle(vertices, rotation_matrix):
    """Rotate all vertices using matrix multiplication"""
    return vertices @ rotation_matrix.T

def full_360_rotation_static():
    """Show rectangle at different angles in one plot"""
    print("=== 360-degree rotation - Static view ===")
    
    rectangle = create_rectangle()
    
    # Create angles for full rotation
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    plt.figure(figsize=(12, 10))
    
    for i, angle in enumerate(angles):
        rotation_matrix = create_rotation_matrix(angle)
        rotated_rectangle = rotate_rectangle(rectangle, rotation_matrix)
        
        # Close the rectangle by adding first vertex at the end
        rotated_closed = np.vstack([rotated_rectangle, rotated_rectangle[0]])
        
        plt.plot(rotated_closed[:, 0], rotated_closed[:, 1], 
                color=colors[i], linewidth=2, marker='o', markersize=6, 
                label=f'{angle}°', alpha=0.8)
    
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('Rectangle at different rotation angles (0° to 315°)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    
    # Add center point
    plt.plot(0, 0, 'ko', markersize=8, label='Rotation Center')
    plt.tight_layout()
    plt.show()

def create_smooth_rotation_animation():
    """Create smooth animation of rotating rectangle"""
    print("\n=== Creating smooth rotation animation ===")
    
    rectangle = create_rectangle()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('Smooth 360° Rectangle Rotation Animation')
    
    # Initialize empty line objects
    line, = ax.plot([], [], 'r-o', linewidth=3, markersize=8)
    angle_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=14)
    
    # Add center point
    ax.plot(0, 0, 'ko', markersize=8, label='Rotation Center')
    ax.legend()
    
    def animate(frame):
        """Animation function called for each frame"""
        # Calculate current angle (0 to 360 degrees)
        current_angle = frame * 5  # 5 degrees per frame
        
        # Create rotation matrix for current angle
        rotation_matrix = create_rotation_matrix(current_angle)
        
        # Rotate rectangle
        rotated_rectangle = rotate_rectangle(rectangle, rotation_matrix)
        
        # Close the rectangle by adding first vertex at the end
        rotated_closed = np.vstack([rotated_rectangle, rotated_rectangle[0]])
        
        # Update the line data
        line.set_data(rotated_closed[:, 0], rotated_closed[:, 1])
        
        # Update angle text
        angle_text.set_text(f'Angle: {current_angle:.1f}°')
        
        return line, angle_text
    
    # Create animation
    # 72 frames * 5 degrees = 360 degrees total
    anim = animation.FuncAnimation(fig, animate, frames=72, 
                                 interval=100, blit=True, repeat=True)
    
    print("Animation created! Close the window to continue...")
    plt.show()
    
    return anim

def step_by_step_rotation():
    """Show step-by-step what happens during rotation"""
    print("\n=== Step-by-step rotation analysis ===")
    
    rectangle = create_rectangle()
    
    # Test specific angles and show the math
    test_angles = [0, 90, 180, 270, 360]
    
    for angle in test_angles:
        print(f"\n--- Rotation at {angle}° ---")
        rotation_matrix = create_rotation_matrix(angle)
        rotated = rotate_rectangle(rectangle, rotation_matrix)
        
        print(f"Rotation matrix:\n{rotation_matrix}")
        print(f"Original vertex 1: {rectangle[0]}")
        print(f"Rotated vertex 1: {rotated[0]}")
        
        # Show the math for first vertex
        x, y = rectangle[0]
        new_x = x * rotation_matrix[0,0] + y * rotation_matrix[0,1]
        new_y = x * rotation_matrix[1,0] + y * rotation_matrix[1,1]
        print(f"Manual calculation: ({new_x:.3f}, {new_y:.3f})")

# Run all demonstrations
if __name__ == "__main__":
    # Show static view of multiple angles
    full_360_rotation_static()
    
    # Show step-by-step analysis
    step_by_step_rotation()
    
    # Create smooth animation
    animation_obj = create_smooth_rotation_animation()
    
    print("\n" + "="*60)
    print("COMPLETE 360° ROTATION ANALYSIS:")
    print("="*60)
    print("✓ Static view: Shows rectangle at 8 different angles")
    print("✓ Step analysis: Shows the math behind key rotations")
    print("✓ Smooth animation: Full 360° continuous rotation")
    print("✓ All using linear algebra - no built-in rotation functions!")
    print("="*60)