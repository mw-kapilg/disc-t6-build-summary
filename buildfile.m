function plan = buildfile
%BUILDFILE Build plan for signal-utils.
import matlab.buildtool.tasks.CodeIssuesTask
import matlab.buildtool.tasks.TestTask

plan = buildplan(localfunctions);

% Put the library on the path so the tests can find it.
addpath(fullfile(plan.RootFolder, "src"));

plan("check") = CodeIssuesTask("src");
plan("test") = TestTask("tests", SourceFiles="src");
plan("test").Dependencies = "check";

plan.DefaultTasks = "test";
end
