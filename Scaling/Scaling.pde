// source image filename
String src_filename = "pic.png";
// target image width
int target_width = 500;
// target image height
int target_height = 200;

// bilinear interpolation
float bilinear(float tx, float ty, int c00, int c01, int c10, int c11) {
    return (1 - tx) * (1 - ty) * c00
            + (1 - tx) * ty * c01
            + tx * (1 - ty) * c10
            + tx * ty * c11;
}

// color -> gray value
int toGray(color c) {
    return int((red(c) + green(c) + blue(c)) / 3);
}

PImage scale(PImage source_img, int target_width, int target_height) {
    PImage target_img = createImage(target_width, target_height, RGB);
    source_img.loadPixels();
    target_img.loadPixels();

    for (int x = 0; x < target_width; x++) {
        for (int y = 0; y < target_height; y++) {
            float gx = (float(x) / target_width) * (source_img.width - 1);
            float gy = (float(y) / target_height) * (source_img.height - 1);
            int gxi = int(gx);
            int gyi = int(gy);
            int gxi_plus = min(gxi + 1, source_img.width - 1);
            int gyi_plus = min(gyi + 1, source_img.height - 1);
            int c00 = toGray(source_img.pixels[gxi + gyi * source_img.width]);
            int c01 = toGray(source_img.pixels[gxi + gyi_plus * source_img.width]);
            int c10 = toGray(source_img.pixels[gxi_plus + gyi * source_img.width]);
            int c11 = toGray(source_img.pixels[gxi_plus + gyi_plus * source_img.width]);
            // set pixel (x, y) in target image
            int gray = int(bilinear(gx - gxi, gy - gyi, c00, c01, c10, c11));
            target_img.pixels[x + target_img.width * y] = color(gray);
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
    target_img = scale(source_img, target_width, target_height);
    target_img.save(str(target_width) + "-" + str(target_height) + ".png");
}

void draw() {
    image(target_img, 0, 0);
}
