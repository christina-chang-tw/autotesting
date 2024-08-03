from typing import List

import libximc.highlevel as ximc

class SettingManager:
    def __init__(self, axis: ximc.Axis):
        self.axis = axis

    def change_move_settings(self, speed: float, accel: float, decel: float) -> None:
        """Set speed, acceleration, and deceleration"""
        move_settings = self.axis.get_move_settings()
        move_settings.Speed = speed
        move_settings.Accel = accel
        move_settings.Decel = decel
        self.axis.set_move_settings(move_settings)

    def change_move_settings_user(self, speed: float, accel: float, decel: float) -> None:
        """Set speed, acceleration, and deceleration of calbriation"""
        move_settings = self.axis.get_move_settings_calb()
        move_settings.Speed = speed
        move_settings.Accel = accel
        move_settings.Decel = decel
        self.axis.set_move_settings_calb(move_settings)

    def change_edges_settings(self, border_flags: ximc.BorderFlags, ender_flags: ximc.EnderFlags, left_border: int, right_border: int, uleft_border: int, uright_border: int):
        """View and configure the limit switch mode."""
        edges_settings = self.axis.get_edges_settings()
        edges_settings.BorderFlags = border_flags
        edges_settings.EnderFlags = ender_flags
        edges_settings.LeftBorder = left_border
        edges_settings.RightBorder = right_border
        edges_settings.uLeftBorder = uleft_border
        edges_settings.uRightBorder = uright_border

    def change_edges_settings_user(self, border_flags: ximc.BorderFlags, ender_flags: ximc.EnderFlags, left_border: float, right_border: float):
        """View and configure the limit switch mode in user unit mode."""
        edges_settings = self.axis.get_edges_settings_calb()
        edges_settings.BorderFlags = border_flags
        edges_settings.EnderFlags = ender_flags
        edges_settings.LeftBorder = left_border
        edges_settings.RightBorder = right_border
        self.axis.set_edges_settings_calb(edges_settings)

    def change_microstep_mode(self, microstep_mode: ximc.MicrostepMode) -> None:
        """Setting the microstep mode. Works only with stepper motors"""
        engine_settings = self.axis.get_engine_settings()
        engine_settings.MicrostepMode = microstep_mode
        self.axis.set_engine_settings(engine_settings)

    def change_user_unit_mode(self, unit: float, microstep_mode: ximc.MicrostepMode) -> None:
        """User unit mode settings"""
        self.axis.set_calb(unit, microstep_mode)

    def change_feedback_settings(self, feedback_type: ximc.FeedbackType,
                                 feedback_flags: ximc.FeedbackFlags) -> None:
        """Feedback settings"""
        feedback_settings = self.axis.get_feedback_settings()
        feedback_settings.FeedbackType = feedback_type
        feedback_settings.FeedbackFlags = feedback_flags
        self.axis.set_feedback_settings(feedback_settings)

    def change_pid_settings(self, kpu: int, kiu: int, kdu: int, kpf: int, kif: int, kdf: int) -> None:
        """ 
        PID settings
        
        Parameters
        ----------
        kpu : int
            Proportional gain for voltage PID routine.
        kiu : int
            Integral gain for voltage PID routine.
        kdu : int
            Differential gain for voltage PID routine.
        kpf : int
            Proportional gain for BLDC position PID routine.
        kif : int
            Integral gain for BLDC position PID routine.
        kdf : int
            Differential gain for BLDC position PID routine.
        """
        pid_settings = self.axis.get_pid_settings()
        pid_settings.KpU = kpu
        pid_settings.KiU = kiu
        pid_settings.KdU = kdu
        pid_settings.Kpf = kpf
        pid_settings.Kif = kif
        pid_settings.Kdf = kdf
        self.axis.set_pid_settings(pid_settings)

    def change_control_sttings(
            self, max_speed: List[int], umax_speed: List[int], timeout: List[int], max_click_time: List[int], flags: ximc.ControlFlags, delta_pos: int, udelta_pos: int
    ) -> None:
        """
        Control settings
        
        Parameters
        ----------
        max_speed : List[int]
            Maximum speed in steps.
        umax_speed : List[int]
            Maximum speed in microsteps.
        timeout : List[int]
            Timeout in ms.
        max_click_time : List[int]
            Maximum click time in ms.
        flags : ximc.ControlFlags
            Control flags.
        delta_pos : int
            Position delta in steps.
        udelta_pos : int
            Position delta in microsteps.
        """
        control_settings = self.axis.get_control_settings()
        control_settings.MaxSpeed = max_speed
        control_settings.uMaxSpeed = umax_speed
        control_settings.Timeout = timeout
        control_settings.MaxClickTime = max_click_time
        control_settings.Flags = flags
        control_settings.DeltaPosition = delta_pos
        control_settings.uDeltaPosition = udelta_pos
        self.axis.set_control_settings(control_settings)

    def change_control_sttings_user(
        self, max_speed: List[float], timeout: List[int], max_click_time: int, flags: ximc.ControlFlags, delta_pos: float
    ) -> None:
        """
        Control settings in user unit mode

        Parameters
        ----------
        max_speed : List[float]
            Maximum speed in user unit.
        timeout : List[int]
            Timeout in ms.
        max_click_time : int
            Maximum click time in s.
        flags : ximc.ControlFlags
            Control flags.
        delta_pos : float
            Position delta in user unit.
        """
        control_settings = self.axis.get_control_settings_calb()
        control_settings.MaxSpeed = max_speed
        control_settings.Timeout = timeout
        control_settings.MaxClickTime = max_click_time
        control_settings.Flags = flags
        control_settings.DeltaPosition = delta_pos
        self.axis.set_control_settings_calb(control_settings)

    
        


