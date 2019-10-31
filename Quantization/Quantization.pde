// source image filename
String src_filename = "pic.png";
// target image gray level
int gray_level = 2;

// color -> gray value
int toGray(color c) {
    return int((red(c) + green(c) + blue(c)) / 3);
}

PImage quantize(PImage source_img, int level) {
    PImage target_img = createImage(source_img.width, source_img.height, RGB);
    source_img.loadPixels();
    target_img.loadPixels();
    
    if (level == 1) {
        for (int x = 0; x < source_img.width; x++) {
            for (int y = 0; y < source_img.height; y++) {
                target_img.pixels[x + target_img.width * y] = color(0);
            }
        }
    }
    else {
        int conversion_factor = 255 / (level - 1);
        
        for (int x = 0; x < source_img.width; x++) {
            for (int y = 0; y < source_img.height; y++) {
                int old_gray = toGray(source_img.pixels[x + y * source_img.width]);
                int new_gray = round(float(old_gray) / conversion_factor) * conversion_factor;
                target_img.pixels[x + target_img.width * y] = color(new_gray);
            }
        }
    }
    
    target_img.updatePixels();
    return target_img;
}

PImage source_img;
PImage target_img;

void setup() {
    fullScreen();
    source_img = loadImage(src_filename);
    target_img = quantize(source_img, gray_level);
    target_img.save("level-" + str(gray_level) + ".png");
}

void draw() {
    image(target_img, 0, 0);
}
