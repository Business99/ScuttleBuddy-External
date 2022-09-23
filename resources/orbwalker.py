import mouse
import time

class Orbwalker:
    MOVE_CLICK_DELAY = 0.05
    ATTACK_SPEED_CAP = 2.5
    
    def __init__(self, client) -> None:
        self.client = client   
        self.can_attack_time = self.client.game_time     
        self.can_move_time = self.client.game_time     
    
    @staticmethod
    def get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap):
        total_attack_speed = min(attack_speed_cap, (champion.attack_speed_multiplier - 1) * attack_speed_ratio + attack_speed_base)
        return 1. / total_attack_speed
    
    @staticmethod
    def get_windup_time(champion, attack_speed_base, attack_speed_ratio, windup_percent, windup_modifier, attack_speed_cap):
        # More information at https://leagueoflegends.fandom.com/wiki/Basic_attack#Attack_speed
        attack_time = Orbwalker.get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap)
        base_windup_time = (1 / attack_speed_base) * windup_percent
        windup_time = base_windup_time + ((attack_time * windup_percent) - base_windup_time) * (1+windup_modifier)
        return min(windup_time, attack_time)
    
    def move_mouse_to_target(self, target): 
        m_pos_x, mouse_pos_y = mouse.get_position()       
        target_x, target_y = target.screen_pos['x'], target.screen_pos['y']
        # diff x
        diff_x = target_x - m_pos_x
        # diff y
        diff_y = target_y - mouse_pos_y        
        mouse.move(diff_x, diff_y, absolute=False, duration=0.1)
        
    def walk(self, target=None, pymeow=None, overlay=None):
        mouse.press(mouse.MIDDLE) 
        
        if target and self.can_attack_time < self.client.game_time:            
            stored_x, stored_y = mouse.get_position()            
            target_wts_pos = pymeow.wts_ogl(overlay, self.client.view_proj_matrix.tolist(), target.gamePos)            
            mouse.move(target_wts_pos['x'],overlay['height'] - target_wts_pos['y'])
            mouse.right_click()    
            time.sleep(0.01)                        
            attack_speed = self.client.get_attack_speed(self.client.localPlayer)
            game_time = self.client.game_time
            attack_speed_base, _ = self.client.get_base_attack_speed(self.client.localPlayer)            
            
            windup_percent, windup_modifier = self.client.get_windup(self.client.localPlayer)
            c_attack_time = 1 / attack_speed
            b_windup_time = (1 / attack_speed_base) * windup_percent
            windup_time = b_windup_time + ((c_attack_time * windup_percent) - b_windup_time) * (1+windup_modifier)
            
            self.can_move_time = game_time + windup_time
            self.can_attack_time = game_time + (1 / attack_speed)
         
            mouse.move(stored_x, stored_y)
        elif self.can_move_time < self.client.game_time:                        
            mouse.right_click()            
            self.can_move_time = self.client.game_time + self.MOVE_CLICK_DELAY
        mouse.release(mouse.MIDDLE)