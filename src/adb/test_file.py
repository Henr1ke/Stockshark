from img_to_FEN import *

white_pawn = cv2.imread('chessPiecesImg/white_pawn.png')
screenshot = cv2.imread('chessPiecesImg/Screenshot_1.png')

pieces = [white_pawn]

pieces = [resize_img(img) for img in pieces]
screenshot = resize_img(screenshot)

pieces_gray = [grayscale_img(img) for img in pieces]
screenshot_gray = grayscale_img(screenshot)

pieces_gray_grad = [morph_grad_img(img) for img in pieces_gray]
screenshot_gray_grad = morph_grad_img(screenshot_gray)

rects1 = [find_template_multiple(screenshot_gray_grad, img) for img in pieces_gray_grad]
print(rects1)

color_list = match_colors(screenshot, pieces, rects1)

color_rect_dict = match_color_rect(rects1, color_list)

print(color_rect_dict)

draw_results_squares(screenshot, color_rect_dict)

board_coords = get_board_coords()
print(board_coords)


# cv2.imshow('Result3', )
# cv2.waitKey(0)
# cv2.destroyAllWindows()
