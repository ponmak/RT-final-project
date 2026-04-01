import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_light as rtl
import RT_texture as rtt
import random

def render_dream_scene():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0 / 9.0
    main_camera.img_width = 1920
    main_camera.samples_per_pixel = 1024
    main_camera.max_depth = 5
    
    
    main_camera.look_from = rtu.Vec3(0, 0, 20)
    main_camera.look_at = rtu.Vec3(0, 0, 0)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    
    main_camera.vertical_fov = 90
    num_spheres = 50
    
    defocus_angle = 3.0
    focus_distance = 15.0
    main_camera.init_camera(defocus_angle, focus_distance)

    world = rts.Scene(cBgcolor=rtu.Color(1.0, 1.0, 1.0))

    color_palette = [
        rtu.Color(1.0, 0.6, 0.8), # ชมพู Pastel สว่าง
        rtu.Color(0.6, 0.8, 1.0), # ฟ้า Pastel สว่าง
        rtu.Color(1.0, 0.95, 0.6),# เหลือง Pastel สว่าง
        rtu.Color(0.7, 1.0, 0.6), # เขียว Pastel สว่าง
        rtu.Color(0.8, 0.6, 1.0), # ม่วง Pastel สว่าง
        rtu.Color(0.5, 0.8, 1.0), # น้ำเงินอ่อนสดใส
        rtu.Color(1.0, 0.8, 0.6), # ส้มอ่อนสว่าง
    ]

    for _ in range(num_spheres):
        x = random.uniform(-9, 9)
        y = random.uniform(-5, 5)
        z = random.uniform(-4, 4)
        center = rtu.Vec3(x, y, z)
        
        radius = random.uniform(0.4, 1.3)
        color = random.choice(color_palette)
        
        mat = rtm.Blinn(color, 1.0, 0.1, 5) 
        world.add_object(rto.Sphere(center, radius, mat))

    red_mat = rtm.Lambertian(rtu.Color(1.0, 0.2, 0.2)) 
    world.add_object(rto.Sphere(rtu.Vec3(1.5, 0.8, 2.0), 0.25, red_mat))

    additional_light = rtl.Diffuse_light(rtu.Color(1.0, 0.8, 0.6))
    world.add_object(rto.Sphere(rtu.Vec3(-2.0, 3.0, 6.0), 0.5, additional_light))

    intg = rti.Integrator(bSkyBG=True) 
    
    renderer = rtren.Renderer(main_camera, intg, world)
    
    renderer.render_jittered()
    
    output_filename = 'bright_dream_recreation_3.png'
    renderer.write_img2png(output_filename) 
    print(f"เรนเดอร์เสร็จสิ้น! บันทึกไฟล์เป็น: {output_filename}")

if __name__ == "__main__":
    render_dream_scene()

