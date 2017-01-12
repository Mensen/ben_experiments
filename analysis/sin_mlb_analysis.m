% corsi block data analysis

% ~~~~~~~~~~~~~
% load the data
% ~~~~~~~~~~~~~

% find all the relevant files
file_list_mlb = swa_getFiles(pwd, {'mlb', 'csv'});
no_files = length(file_list_mlb);

% get experiment info from filename
full_table = table();

% pre-allocate
no_correct = nan(no_files, 1);
best_effort = nan(no_files, 1);
mean_time = nan(no_files, 1);
participant_id = cell(no_files, 1);

% load them all
for n_file = 1 : no_files
    
    % get participant id from filename
    [filePath, fileName, ext] = fileparts(file_list_mlb{n_file});
    participant_id{n_file} = fileName(12:13);
    
    % import the data as a table
    imported_data = readtable(file_list_mlb{n_file}, 'delimiter', ',');
    
    % convert the string times into digits
    block_number = repmat(imported_data.block_number, 1, 8)';
    x_pos = cell2mat(cellfun(@(x) str2num(x), imported_data.x_pos, 'uni', 0)')';
    y_pos = cell2mat(cellfun(@(x) str2num(x), imported_data.y_pos, 'uni', 0)')';
    trial_length = cell2mat(cellfun(@(x) str2num(x), imported_data.length, 'uni', 0')')';
    trial_error = cell2mat(cellfun(@(x) str2num(x), imported_data.error, 'uni', 0)')';
    trial_time = cellfun(@(x) str2num(x), imported_data.trial_time, 'uni', 0);
    trial_time = cell2mat(cellfun(@(x) [x(1) diff(x)], trial_time, 'uni', 0)')';
    
    % put in the full_table
    full_table = [full_table; table(...
        block_number(:), x_pos, y_pos, trial_length, trial_error, trial_time, ...
        'variableNames', ...
        {'block', 'x_pos', 'y_pos', 'length', 'error', 'time'})];
    
end

% put participants into a table
temp = repmat(participant_id, 1, 40)';
full_table.participant_id = temp(:);
full_table.abs_error = abs(full_table.error);

% ~~~~~~~~~~~~~~~~
% plot the results
% ~~~~~~~~~~~~~~~~
% select subset of data if desired
selected_rows = 1:size(full_table, 1);
% selected_rows = full_table.number_correct > 4 & ~full_table.flag_classic;

% plot the grouped scatter plot
handles = group_scatter_plot(full_table(selected_rows, :), 'error', 'y_pos');


% correlation analysis
% ^^^^^^^^^^^^^^^^^^^^
selected_rows = 1:size(full_table, 1);
% selected_rows = ~isnan(full_table.time) & full_table.time < 3;
x_values = full_table(selected_rows, :).length * 13;
y_values = abs(full_table(selected_rows, :).time);

handles.figure = figure('color', 'w', ...
    'position', [200, 200, 500, 500]);
handles.axes = axes('nextplot', 'add');
scatter(x_values, y_values, 'fill', ...
    'sizeData', 60 ,...
    'markerEdgeColor', 'k');

% line of best fit
coeffs = polyfit(x_values, y_values, 1);
% Get fitted values
fittedX = [min(x_values), max(x_values)];
fittedY = polyval(coeffs, fittedX);
% Plot the fitted line
plot(fittedX, fittedY, 'k-', 'LineWidth', 2);

% % make a text box of stats
% [r_value, p_,] = corr(x_values, y_values);
% text(mean(x_values), max(y_values),...
%     sprintf('r = %0.3f\np = %0.3f', r_value, p_),...
%     'edgeColor', 'k', ...
%     'horizontalAlignment', 'center');

export_fig(gcf, ['scatter_correlation'], '-pdf');


% ~~~~~~~~~~~~~~~~~
% proper statistics
% ~~~~~~~~~~~~~~~~~
model_description = ...
    'time ~ length + (1 | participant_id)';

full_model = fitlme(full_table, model_description);