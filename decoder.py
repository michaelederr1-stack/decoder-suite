def _get_best_axis_move(self, current, target, max_bounds, inc_cmd, dec_cmd):
        """Calculates standard vs wrapped delta and returns minimal path sequence."""
        diff = target - current
        standard_dist = abs(diff)
        standard_cmds = [inc_cmd] * diff if diff > 0 else [dec_cmd] * abs(diff)

        if not self.enable_wrapping or max_bounds <= 0:
            return standard_cmds

        # Toroidal wrapping math
        if diff > 0:
            wrap_dist = (current + max_bounds) - target
            wrap_cmds = [dec_cmd] * wrap_dist
        else:
            wrap_dist = (target + max_bounds) - current
            wrap_cmds = [inc_cmd] * wrap_dist

        if wrap_dist < standard_dist:
            return wrap_cmds
        return standard_cmds

