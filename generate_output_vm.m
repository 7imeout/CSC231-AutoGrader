%% init
clear;
format short;
format compact;
    
%% import working directories
dirs = importdata('./dir_VM.dat');

%% cd to results dir
cd(char(dirs(1)));

%% clean up previous output
delete('*.txt');

%% cd to working dir
cd(char(dirs(2)));

%% get labs to grade (written by Python)
labs = importdata('./lab_list.dat');
num_labs = length(labs);

for l = 1:num_labs
    % re-load labs to grade and cd to next lab dir
    labs = importdata('./lab_list.dat');
    lab_str = char(labs(l));
    lab_dir = lab_str(1:length(lab_str) - 2);
    cd(strcat('./', lab_dir));

    % generate list of directories within each lab dir
    dir_list = dir('./');
    dirs = {dir_list(:).name}';
    dirs = dirs(endsWith(dirs, '_file_'));

    % write directory listing to file
    fileID = fopen('./../dir_list.dat','w');
    [nrows,~] = size(dirs);
    for row = 1:nrows
        fprintf(fileID,'%s\n',dirs{row,:});
    end
    fclose(fileID);
    
    % cd back up to working dir
    cd ../

    % write lab currently being graded to file
    fid = fopen('./lab.dat','wt');
    fprintf(fid, lab_str);
    fclose(fid);
    
    % loop for a single lab, multiple students
    fprintf('Genering outputs for: %s ...\n', lab_str);
    for n = 1:length(dirs)
        % reload directory (student) listing
        if ~exist('dirs', 'var')
            dirs = importdata('./dir_list.dat');
        end
        
        % reload current lab information
        io_contents = fullfile('./lab.dat');
        lab_str = fileread(io_contents);
        lab_dir = lab_str(1:5);
        dir_str = char(dirs(n));
        
        % go into individual student's directory
        path = strcat('./', lab_dir, '/', dir_str, '/');
        cd(path); 

        % extract student name, replace space with _
        delim_ndx = strfind(dir_str, '_');
        student_name = dir_str(1:delim_ndx(1)-1);
        student_name(strfind(student_name, ' ')) = '_';

        fprintf(strcat('\n---------v-----[ %s | %s ]-----v---------\n\n'), ...
            student_name, lab_str);

        % output filename format is First_Last_labXX.txt
        output_filename = strcat(student_name, '_', lab_dir, '.txt');
        diary(strcat('../../../results/', output_filename));

        % run student code and save output (including stderr) to file
        try
            if exist(lab_str, 'file') == 2
                eval(lab_dir);
                who;
            end
        catch exc
           report = getReport(exc); 
           display(report);
        end

        diary off;
        fprintf('---------^----------^----------^----------^---------\n\n');

        cd ../../
        dirs = importdata('./dir_list.dat');
    end
end

%% cleanup
clear;
delete('*.dat');
clc;
