package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;

public class AutoAimCommand extends Command {

    public AutoAimCommand() {
        requires(Robot.intakeLauncher);
    }

    protected void initialize() {
        Robot.intakeLauncher.toggleAutoAim();
    }

    protected void execute() {

    }

    protected boolean isFinished() {
        return !Robot.intakeLauncher.getAutoAim();
    }

    protected void end() {

    }

    protected void interrupted() {

    }
}