import React, { Component } from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { mapToCssModules } from 'reactstrap/lib/utils';

const propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  cssModule: PropTypes.object,
  dataBox: PropTypes.func,
};

const defaultProps = {
  dataBox: () => ({ variant: 'facebook', friends: '-', feeds: '-' }),
};

class Widget05 extends Component {
  render() {

    // eslint-disable-next-line
    const { children, className, cssModule, dataBox, ...attributes } = this.props;

    // demo purposes only
    const data = dataBox();
    const variant = data.variant;

    if (!variant || ['facebook', 'twitter', 'linkedin', 'google-plus', 'fomular'].indexOf(variant) < 0) {
      return (null);
    }

    const back = 'bg-' + variant;
    const icon = 'fa fa-' + variant;
    const keys = Object.keys(data);
    const vals = Object.values(data);

    const classCard = 'brand-card';
    const classCardHeader = classNames(`${classCard}-header`, back);
    const classCardBody = classNames(`${classCard}-body`);
    const classes = mapToCssModules(classNames(classCard, className), cssModule);

    return (
      <div className={classes}>
        <div className={classCardHeader}>
        <div className="text-value">Fomular</div>
        </div>
        <div className={classCardBody}>
          <div>
            <div className="text-value">{vals[1]}</div>
            <div className="text-uppercase text-muted small">{keys[1]}</div>
          </div>
          <div>
            <div className="text-value">{vals[2]}</div>
            <div className="text-uppercase text-muted small">{keys[2]}</div>
          </div>
        </div>
      </div>
    );
  }
}

Widget05.propTypes = propTypes;
Widget05.defaultProps = defaultProps;

export default Widget05;
