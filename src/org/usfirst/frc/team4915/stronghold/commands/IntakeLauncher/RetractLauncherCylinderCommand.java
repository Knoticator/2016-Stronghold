package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;

public class RetractLauncherCylinderCommand extends Command {

    // this command pulls back the cylinder that launches the ball
    public RetractLauncherCylinderCommand() {
        requires(Robot.intakeLauncher);
    }

    @Override
    protected void initialize() {
        Robot.intakeLauncher.retractCylinder();
    }

    @Override
    protected void execute() {

    }

    @Override
    protected boolean isFinished() {
        return true;
    }

    @Override
    protected void end() {
        isFinished();
    }

    @Override
    protected void interrupted() {
        
    }

}
