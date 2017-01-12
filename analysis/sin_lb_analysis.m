% corsi block data analysis

% ~~~~~~~~~~~~~
% load the data
% ~~~~~~~~~~~~~

% find all the relevant files
file_list_cb = swa_getFiles(pwd, {'_lb', 'csv'});
no_files = length(file_list_cb);

% pre-allocate
full_table = table();
participant_id = cell(no_files, 1);
mean_error = nan(no_files, 1);
mean_time = nan(no_files, 1);

% load them all
for n_file = 1 : no_files
    
    % get participant id from filename
    [filePath, fileName, ext] = fileparts(file_list_cb{n_file});
    participant_id{n_file} = fileName(11:12);
    
    % import the data as a table
    imported_data = readtable(file_list_cb{n_file});
    
    if size(imported_data, 2) < 6
        imported_data = [imported_data, table(nan(40, 1), ...
            'variableName', {'time'})];
        imported_data.Properties.VariableNames{'Var5'} = 'Var6';
    end
    
    full_table = [full_table; imported_data];
    
    mean_error(n_file) = mean(imported_data.error);
    mean_time(n_file) = mean(imported_data.time);
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
selected_rows = full_table.number_correct > 4;

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
