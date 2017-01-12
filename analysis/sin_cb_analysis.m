% corsi block data analysis

% ~~~~~~~~~~~~~
% load the data
% ~~~~~~~~~~~~~

% find all the relevant files
file_list_cb = swa_getFiles(pwd, {'cb', 'csv'});
no_files = length(file_list_cb);

% split paths and filenames
[pathstr, name, ext] = fileparts(file_list_cb) 


% get experiment info from filename
full_table = table();
full_table = [full_table, table(cell(no_files, 1), ...
    'variableName', {'participant_id'})];
full_table = [full_table, table(cellfun(@(x) any(regexp(x, '_c_')), file_list_cb), ...
    'variableName', {'flag_classic'})];
full_table = [full_table, table(cellfun(@(x) any(regexp(x, '_r')), file_list_cb), ...
    'variableName', {'flag_reverse'})];
full_table = [full_table, table(nan(no_files, 1), ...
    'variableName', {'number_correct'})];
full_table = [full_table, tablenan(no_files, 1), ...
    'variableName', {'best_effort'})];
full_table = [full_table, tablenan(no_files, 1), ...
    'variableName', {'mean_time'})];

% pre-allocate
no_correct = nan(no_files, 1);
best_effort = nan(no_files, 1);
mean_time = nan(no_files, 1);
participant_id = cell(no_files, 1);

% load them all
for n_file = 1 : no_files
    
    % get participant id from filename
    [filePath, fileName, ext] = fileparts(file_list_cb{n_file});
    participant_id{n_file} = fileName(13:14);
    
    % import the data as a table
    imported_data = readtable(file_list_cb{n_file});
    
    % convert the string times into digits
    trial_times = cellfun(@(x) str2num(x), imported_data.trial_time, 'uni', 0);
    
    % get the maximum correct (and best after after)
    [full_table.number_correct(n_file) , max_ind] = ...
        max(imported_data.number_correct);
    full_table.best_effort(n_file) = max(imported_data.number_correct(max_ind(1) + 1:end)) / [no_correct(n_file) + 1];
   
    % calculate mean time for last correct
    full_table.mean_time(n_file) = mean(diff(trial_times{max_ind(1)}));
    
end

% put participants into a table
full_table.participant_id = participant_id;

% ~~~~~~~~~~~~~~~~
% plot the results
% ~~~~~~~~~~~~~~~~
% select subset of data if desired
selected_rows = 1:size(full_table, 1);
% selected_rows = full_table.number_correct > 4 & ~full_table.flag_classic;
selected_rows = full_table.number_correct > 4;

% plot the grouped scatter plot
handles = group_scatter_plot(full_table(selected_rows, :), 'number_correct', 'flag_reverse');


% correlation analysis
% ^^^^^^^^^^^^^^^^^^^^
x_values = full_table.number_correct;
y_values = full_table.best_effort;

handles.figure = figure('color', 'w', ...
    'position', [200, 200, 500, 500]);
handles.axes = axes('nextplot', 'add');
scatter(x_values, y_values, 'fill', ...
    'sizeData', 60 ,...
    'markerEdgeColor', 'k');

% line of best fit
coeffs = polyfit(x_values, y_values, 1)
% Get fitted values
fittedX = [min(x_values), max(x_values)];
fittedY = polyval(coeffs, fittedX);
% Plot the fitted line
plot(fittedX, fittedY, 'k-', 'LineWidth', 2);

% make a text box of stats
text(mean(x_values), min(y_values),...
    sprintf('r = %0.3f\np = %0.3f', r_value, p_),...
    'edgeColor', 'k', ...
    'horizontalAlignment', 'center');

export_fig(gcf, ['scatter_correlation'], '-pdf');