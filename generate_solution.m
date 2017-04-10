%% init
clear;
format short;
format compact;
    
%% working directory is ./solutions/source
cd('./solutions/source/');

%% get labs to grade (written by Python)
labs = importdata('./../../submissions/lab_list.dat');
num_labs = length(labs);

for l = 1:num_labs
    lab_file_str = char(labs(l));
    lab_name_str = lab_file_str(1:length(lab_file_str) - 2);
    
    fprintf('Genering a solution for: %s ...\n\n', lab_file_str);

    % output filename format is labXX.out.txt
    output_filename = strcat('../', lab_name_str, '.out.txt');
    
    % clean up existing outputs before outputting new
    delete(output_filename);
    diary(output_filename);

    try % run solution source code and save output
        if exist(lab_file_str, 'file') == 2
            eval(lab_name_str);
            who;
        end
    catch exc
       report = getReport(exc); 
       display(report);
    end

    diary off;
    
    % reload lab list as it got cleared by solution
    labs = importdata('./../../submissions/lab_list.dat');
end

%% cleanup
clear;
